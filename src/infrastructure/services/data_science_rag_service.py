from typing import List, Iterable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from pathlib import Path
from langchain_core.documents import Document

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataScienceRAGService:
    def __init__(self, chroma_path: str = "./chroma_db", embedding_model: str = "mxbai-embed-large", llm_model: str = "gemma3:12b", ollama_base_url: str = "http://ollama:11434", temperature: float = 0.5, k_docs: int = 10):
        self.chroma_path = Path(chroma_path)
        self.k_docs = k_docs
        logger.info("Init components...")
        self._init_components( embedding_model, llm_model, ollama_base_url,  temperature)
        logger.info("Ensuring embeddings...")
        self._ensure_embeddings()
        logger.info("Init RAG chain...")
        self._init_chain()

    def _init_components(self, embedding_model: str, llm_model: str, ollama_base_url: str, temperature: float):
        try:
            logger.info(f"Creating Ollama embeddings model={embedding_model}")
            self.embedding_function = OllamaEmbeddings(
                model=embedding_model,
                base_url=ollama_base_url
            )

            logger.info(f"Creating ChatOllama model={llm_model}")
            self.llm = ChatOllama(
                model=llm_model,
                temperature=temperature,
                base_url=ollama_base_url
            )

            logger.info(f"Opening Chroma DB at {self.chroma_path}")
            self.vectorstore = Chroma(
                persist_directory=str(self.chroma_path),
                embedding_function=self.embedding_function
            )

        except Exception:
            logger.exception("Failed during _init_components")
            raise

    def _ensure_embeddings(self) -> None:
        try:
            logger.info("Checking existing embeddings in Chroma")
            try:
                existing_count = self.vectorstore._collection.count()
                logger.info(f"Existing embeddings: {existing_count}")
            except Exception:
                logger.warning("Could not count existing embeddings, assuming empty")
                existing_count = 0

            if existing_count > 0:
                logger.info("Embeddings already exist, skipping indexing")
                return

            data_dir = Path(__file__).resolve().parent / "data"
            logger.info(f"Looking for data directory at {data_dir}")

            if not data_dir.exists():
                logger.warning("Data directory does not exist, skipping embeddings")
                return

            docs = list(self._load_documents_from_dir(data_dir))
            logger.info(f"Loaded {len(docs)} documents")

            if not docs:
                logger.warning("No documents found, skipping embeddings")
                return

            chunks = self._split_documents(docs, chunk_size=400, chunk_overlap=100)
            logger.info(f"Split into {len(chunks)} chunks, adding to vectorstore")

            self.vectorstore.add_documents(chunks)
            logger.info("Embeddings successfully added to vectorstore")

            if hasattr(self.vectorstore, "persist"):
                try:
                    self.vectorstore.persist()
                    logger.info("Chroma DB persisted")
                except Exception:
                    logger.exception("Failed to persist Chroma DB")

        except Exception:
            logger.exception("Failed during _ensure_embeddings")
            raise

    @staticmethod
    def _load_documents_from_dir(data_dir: Path) -> Iterable[Document]:
        for path in sorted(data_dir.glob("**/*")):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = path.read_text(encoding="utf-8", errors="ignore")
            yield Document(page_content=text, metadata={"source": str(path)})

    @staticmethod
    def _split_documents(docs: List[Document], chunk_size: int = 1000, chunk_overlap: int = 150) -> List[Document]:
        if chunk_size <= 0:
            return docs
        if chunk_overlap < 0:
            chunk_overlap = 0

        chunks: List[Document] = []
        step = max(chunk_size - chunk_overlap, 1)

        for doc in docs:
            text = doc.page_content
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunk_text = text[start:end]
                if chunk_text.strip():
                    chunks.append(
                        Document(
                            page_content=chunk_text,
                            metadata=dict(doc.metadata)
                        )
                    )
                start += step

        return chunks

    def _init_chain(self):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": self.k_docs})

        system_prompt = ChatPromptTemplate.from_template("""
You are an expert assistant for a Big Data / Data Science course. You primarily rely on the lecture materials provided in <context>.

Your goals:
1) Give correct, concise answers about the lecture topics.
2) If the lecture context is insufficient but the question is still on-topic (Big Data / Data Science), you may use your general knowledge to fill gaps. Mark this clearly as general knowledge, not from the lectures.
3) If the question is clearly off-topic (not related to Big Data / Data Science), refuse politely and say you do not answer such questions.

Rules:
- Think through the answer internally, but do NOT reveal chain-of-thought.
- Cite lecture content implicitly by paraphrasing it; do not invent details.
- When using general knowledge, explicitly label it as "General knowledge".
- Detect the user's language and respond in that language.
- If the context is empty or irrelevant, follow rule #2 or #3 accordingly.

Output format:
...final response...

<context>
{context}
</context>

Question: {question}
""")

        self.rag_chain = (
                {
                    "context": retriever | self.format_docs,
                    "question": RunnablePassthrough()
                }
                | system_prompt
                | self.llm
                | StrOutputParser()
        )

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self, question: str) -> str:
        return self.rag_chain.invoke(question)

    async def stream_ask(self, question: str):
        async for chunk in self.rag_chain.astream(question):
            yield chunk

    def get_relevant_docs(self, question: str, k: int = 3) -> List[str]:
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        docs = retriever.invoke(question)
        return [doc.page_content for doc in docs]

    def close(self):
        if hasattr(self.vectorstore, '_client'):
            self.vectorstore._client.close()
