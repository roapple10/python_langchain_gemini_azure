# CH15-1: RAG with LangServe (Google Gemini API)

這是一個使用 Google Gemini API 的 RAG（Retrieval-Augmented Generation）應用程式，透過 LangServe 提供 REST API 服務。

## 專案結構

```
ch15-1/
├── ch15-1/                    # 獨立執行的 RAG 腳本
│   ├── __init__.py
│   ├── rag.py                 # 載入 PDF 並建立向量資料庫
│   └── requirements.txt
├── langserveapp/              # LangServe API 服務
│   ├── app/
│   │   ├── __init__.py
│   │   └── server.py          # FastAPI 伺服器
│   ├── rag/
│   │   ├── __init__.py
│   │   └── rag_chain.py       # RAG Chain 定義
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── tests/
│   └── __init__.py
├── qa.pdf                     # 問答資料 PDF
└── README.md                  # 本文件
```

## 環境變數

`.env` 檔案位於 `python_langchain_gemini_azure/.env`，需要包含以下變數：

```env
GOOGLE_API_KEY=你的_Google_API_金鑰
GEMINI_MODEL_ID=gemini-2.0-flash
QDRANT_URL=你的_Qdrant_URL
QDRANT_API_KEY=你的_Qdrant_API_金鑰
```

---

## 執行步驟

### 步驟 1：建立向量資料庫

先將 PDF 資料載入到 Qdrant 向量資料庫：

```bash
cd python_langchain_gemini_azure/CH15/ch15-1

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 安裝依賴並執行
pip install -r ch15-1/requirements.txt
python ch15-1/rag.py
```

### 步驟 2：建立並執行 Docker

```bash
# 進入 langserveapp 目錄
cd langserveapp

# 建立 Docker Image
docker build -t ch15-langserve-app .

# 執行 Docker Container（掛載 .env 檔案）
docker run -d \
  --name ch15-langserve \
  -p 8080:8080 \
  -v $(pwd)/../../../.env:/code/.env:ro \
  ch15-langserve-app
```

### 步驟 3：測試 API

```bash
# 開啟 LangServe Playground（推薦）
http://localhost:8080/rag/playground/

# 或使用 curl 測試
curl -X POST "http://localhost:8080/rag/invoke" \
  -H "Content-Type: application/json" \
  -d '{"input": {"input": "請問第二胎補助加發多少，共為多少錢？"}}'
```

### 步驟 4：停止與清理

```bash
docker stop ch15-langserve
docker rm ch15-langserve
```

---

## 技術棧

- **LLM**: Google Gemini API (`gemini-flash-lite-latest`)
- **Embeddings**: Google Gemini Embeddings (`gemini-embedding-001`)
- **Vector Store**: Qdrant
- **Framework**: LangChain + LangServe
- **Web Framework**: FastAPI + Uvicorn
