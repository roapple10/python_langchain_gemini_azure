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

---

## 程式碼說明

### 1. `ch15-1/rag.py` - 向量資料庫建立腳本

此腳本負責將 PDF 文件載入並存入 Qdrant 向量資料庫，是執行 RAG 前的資料準備步驟。

**主要功能：**
1. **載入 PDF 文件** - 使用 `PyPDFLoader` 讀取 `qa.pdf` 檔案
2. **分割文本** - 使用 `RecursiveCharacterTextSplitter` 將文件分割為 500 字元的區塊，重疊 100 字元
3. **建立 Embeddings** - 使用 Google Gemini Embeddings (`gemini-embedding-001`) 將文本轉換為向量
4. **存入向量資料庫** - 將向量存入 Qdrant 的 `subsidy_qa` collection（每次執行會重建）
5. **測試查詢** - 建立 Retrieval Chain 並執行一個測試問題驗證功能


---

### 2. `langserveapp/app/server.py` - FastAPI 伺服器

此檔案定義 FastAPI 應用程式並整合 LangServe，提供 REST API 服務。

**主要功能：**
1. **建立 FastAPI 應用程式** - 初始化 FastAPI 實例
2. **根路徑重導向** - 訪問根路徑時自動導向 `/docs` API 文件頁面
3. **掛載 RAG Chain** - 使用 `add_routes()` 將 RAG Chain 掛載到 `/rag` 路徑

**LangServe 自動產生的端點：**
| 端點 | 說明 |
|------|------|
| `POST /rag/invoke` | 同步呼叫 RAG Chain |
| `POST /rag/batch` | 批次呼叫 |
| `POST /rag/stream` | 串流回應 |
| `GET /rag/playground/` | 互動式測試介面 |

---

### 3. `langserveapp/rag/rag_chain.py` - RAG Chain 定義

此檔案定義 LangServe 使用的 RAG Chain，連接已建立的 Qdrant 向量資料庫進行問答。

**主要功能：**
1. **連接 Qdrant** - 使用 `QdrantClient` 連接已存在的 `subsidy_qa` collection
2. **建立 Retriever** - 設定每次查詢取回最相關的 3 筆文件 (k=3)
3. **定義 Prompt Template** - 建立包含 context 與問題的 Prompt 格式
4. **組合 Chain** - 使用 `create_stuff_documents_chain` 與 `create_retrieval_chain` 組合完整的 RAG Chain
5. **型別定義** - 使用 Pydantic `BaseModel` 定義輸入格式，供 LangServe 自動生成 API Schema

**RAG 處理流程：** 使用者問題 → Qdrant 向量搜尋取得相關文件 → 組合 Prompt → Gemini LLM 生成回答 → 回傳答案

---

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

# 啟動虛擬環境 (macOS/Linux)
source venv/bin/activate

# 啟動虛擬環境 (Windows)
# 在 PowerShell 中執行下列指令啟用 venv，並避免執行權限問題
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\venv\Scripts\Activate.ps1

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

# (macOS/Linux)
curl -X POST "http://localhost:8080/rag/invoke" \
  -H "Content-Type: application/json" \
  -d '{"input": {"input": "請問第二胎補助加發多少，共為多少錢？"}}'

# (Windows)
Invoke-RestMethod `
  -Uri "http://localhost:8080/rag/invoke" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "input": {
      "input": "請問第二胎補助加發多少，共為多少錢？"
    }
  }'



```

# (macOS/Linux)


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

---

## API Response 說明

### 1. Input（使用者輸入）

```json
{
  "input": "請問第二胎補助加發多少，共為多少錢？"
}
```

- 代表使用者問的問題
- RAG 系統會根據這句話去查向量資料庫內容

---

### 2. Context（模型找到的來源文件）

```json
"context": [
  { "metadata": {...}, "page_content": "..." },
  { "metadata": {...}, "page_content": "..." },
  ...
]
```

#### Context 內容結構

| 欄位類型 | 欄位名稱 | 說明 | 範例 |
|---------|---------|------|------|
| **metadata** | `source` | 文件路徑 | `qa.pdf` |
| **metadata** | `page` | 來源 PDF 的頁碼 | `1` |
| **metadata** | `_id` | 向量資料庫中該段內容的 ID | `abc123...` |
| **metadata** | `_collection_name` | 放進資料庫的集合名稱 | `subsidy_qa` |
| **page_content** | - | 文件文字內容，RAG 根據這些文字生成回答 | `第2名子女即加發：第2名子女加發1,000元...` |

> 📌 這些資訊用來追蹤內容從哪裡來，方便除錯或標註來源。

---

### 3. Answer（模型串流回傳的回答）

```json
{ "answer": "根據提供的資訊" }
{ "answer": "，第二名子女的補助加發金額如下：" }
{ "answer": "發金額：第2名子女加發 1,000 元。" }
...
```

| 特性 | 說明 |
|-----|------|
| 回傳模式 | LLM Streaming（串流）模式 |
| 輸出方式 | 每次回傳一小段文字 |
| 完整回答 | 需將所有 `answer` 合併後才是完整回答 |

---

### 4. 完整 Response 結構總覽

| 欄位 | 類型 | 說明 |
|-----|------|------|
| `input` | `string` | 使用者輸入的問題 |
| `context` | `array` | 從向量資料庫檢索到的相關文件列表 |
| `context[].metadata` | `object` | 文件的來源資訊（source、page、_id、_collection_name） |
| `context[].page_content` | `string` | 文件的實際文字內容 |
| `answer` | `string` | LLM 根據 context 生成的回答（串流模式下分段回傳） |

---

