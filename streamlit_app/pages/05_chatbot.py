import streamlit as st
import websocket
import time 

st.set_page_config(page_title="Vitalik Chatbot", page_icon="🤖", layout="wide")
st.title("Vitalik Chatbot")

WS_URL = "ws://host.docker.internal:8000/chatbot/ws"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])


def get_sync_response(prompt: str, ws_url: str):
    """
    Синхронный генератор.
    Убрал ws.close(), так как он вызывает WinError 10013 в новых версиях библиотеки.
    """
    full_response = ""
    try:
        ws = websocket.create_connection(ws_url)
        ws.send(prompt)
        
        while True:
            chunk = ws.recv()
            if chunk == "[DONE]":
                break
            
            if chunk.startswith("[ERROR]"):
                full_response += chunk
                break
            
            full_response += chunk
            yield full_response

            time.sleep(0.05)
            
    except ConnectionRefusedError:
        yield "Сервер отклонил соединение."
    except Exception as e:
        yield f"Ошибка: {e}"
    


if prompt := st.chat_input("Задайте вопрос..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})

    with st.chat_message("assistant", avatar="😈"):
        response_placeholder = st.empty()
        partial_text = ""
        
        for partial_text in get_sync_response(prompt, WS_URL):
            response_placeholder.markdown(partial_text + "▌")
        
        response_placeholder.markdown(partial_text)

    st.session_state.messages.append({"role": "assistant", "content": partial_text, "avatar": "😈"})