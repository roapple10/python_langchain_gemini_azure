FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY ./rag ./rag

# .env 檔案應透過 docker run -v 掛載，而非複製到 image 中
# 這樣可以避免將敏感資訊打包到 image

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080

