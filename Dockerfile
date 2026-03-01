FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# для винды поменять на java-21-openjdk-amd64
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-arm64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV SPARK_LOCAL_IP=127.0.0.1

WORKDIR /app

COPY requirements.txt .

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
