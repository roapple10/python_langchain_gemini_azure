# Streamlit + Gemini LLM App

這是一個使用 Streamlit、LangChain 和 Google Gemini API 建立的簡單 LLM 應用。

## 功能

- 使用 Google Gemini API 生成文字回應
- 簡潔的 Streamlit 介面
- 支援自訂輸入提示

## 安裝

### 使用 Poetry（推薦）

```bash
# 安裝依賴
poetry install

# 啟動虛擬環境
poetry shell
```

### 使用 pip

```bash
pip install -r requirements.txt
```

## 設定

支援兩種方式設定 API Key：

### 方式 1：使用 .env 檔案（推薦）

1. 在 `LLM_app` 目錄中建立 `.env` 檔案：
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   GEMINI_MODEL_ID=gemini-2.0-flash-exp
   ```

2. 取得 Google API Key: https://aistudio.google.com/app/apikey

### 方式 2：直接在應用介面輸入

啟動應用後，在側邊欄輸入您的 Google API Key（如果已設定 .env，會自動載入）

## 執行應用

```bash
# 使用 Poetry
poetry run streamlit run streamlit_app.py

# 或直接使用 streamlit
streamlit run streamlit_app.py
```

應用會在瀏覽器中自動開啟，預設網址為 `http://localhost:8501`

## 使用方式

1. 在側邊欄輸入您的 Google API Key（或事先在 .env 檔案中設定）
2. 選擇想要使用的 Gemini 模型（Flash 或 Pro）
3. 在文字區域輸入您想要詢問的問題
4. 點擊「送出」按鈕
5. 等待 Gemini 生成回應

## 檔案結構

```
LLM_app/
├── streamlit_app.py      # 主要應用程式
├── pyproject.toml         # Poetry 依賴管理
├── requirements.txt       # pip 依賴清單
├── .env.example          # 環境變數範例
└── README.md             # 說明文件
```

## 技術棧

- **Streamlit**: 前端介面框架
- **LangChain**: LLM 應用開發框架
- **Google Gemini**: 大型語言模型 API
- **Poetry**: Python 依賴管理工具

## ✨ 特色

- ✅ 簡潔易用，約 50 行程式碼
- ✅ 使用 Gemini API（比 OpenAI 更經濟實惠）
- ✅ 支援中文介面
- ✅ 使用 Poetry 管理依賴
- ✅ 支援從 .env 檔案或介面輸入 API Key
- ✅ 可選擇不同的 Gemini 模型（Flash、Pro 等）
- ✅ 參考了 `demo5-1_gemini.py` 的 API 設定方式

