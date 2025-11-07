# CH6 - RAG with History（帶有歷史記錄的檢索增強生成）

本章節展示如何實現帶有對話歷史記錄的 RAG (Retrieval-Augmented Generation) 系統，使用向量資料庫進行文件檢索，並結合對話記憶功能。這是一個進階的應用，結合了文件檢索、向量資料庫、語言模型和持久化對話記憶。

## 🎯 本章學習目標

- ✅ 理解 RAG（檢索增強生成）的運作原理
- ✅ 學習使用 WebBaseLoader 載入網頁資料
- ✅ 掌握文件分割（Document Splitting）技術
- ✅ 學習向量嵌入（Embeddings）與向量資料庫（Qdrant）
- ✅ 實作對話歷史記憶（Chat History with SQLite）
- ✅ 整合檢索鏈與對話記憶
- ✅ 比較 Azure OpenAI 與 Google Gemini 在 RAG 中的應用

## 🔑 API 申請教學

在開始學習前，您需要先取得 AI 模型的 API Key。以下提供兩種選擇：

### 方案一：Azure OpenAI Service（有限制條件）

Azure OpenAI 提供 $200 美金的免費額度，但有**嚴格的限制條件**：

⚠️ **重要限制：必須是全新帳號才能使用免費額度**
- **全新的電話號碼**（之前未註冊過 Azure 服務）
- **全新的信用卡**（之前未綁定過 Azure 帳號）
- **全新的電子信箱**（之前未使用過 Azure 服務）

如果您曾經使用過 Azure 任何服務，即使是免費試用，都**無法再次申請免費額度**。

#### Azure OpenAI 申請步驟

1. 前往 [Azure Portal](https://portal.azure.com/)
2. 使用全新的 Microsoft 帳號註冊
3. 提供信用卡資訊（僅用於驗證，不會自動扣款）
4. 建立 Azure OpenAI 資源
5. 部署 GPT 模型和 Embeddings 模型
6. 取得 Endpoint 和 API Key

詳細教學請參考：[Azure OpenAI Service 申請教學](https://ithelp.ithome.com.tw/m/articles/10353046)

**如果您不符合全新帳號條件，請改用下方推薦的 Google AI Studio**

---

### 方案二：Google AI Studio API（✨ 推薦）

**為什麼推薦使用 Google AI Studio？**

✅ **完全免費**：無需綁定信用卡  
✅ **設定簡單**：5 分鐘內完成申請  
✅ **無帳號限制**：任何 Google 帳號都能使用  
✅ **慷慨的免費額度**：每分鐘 15 個請求，足夠學習使用  
✅ **強大的 Gemini 模型**：效能媲美 GPT-4  
✅ **內建 Embeddings**：免費的 gemini-embedding-001 模型

#### Google AI Studio 申請步驟（5 步驟完成）

**第一步**：前往 [Google AI Studio](https://ai.google.dev)，點擊藍色按鈕「Explore models in Google AI Studio」

**第二步**：勾選第一個選項，並點擊「I accept」同意條款

**第三步**：點擊右上角的「Get API key」按鈕

**第四步**：點擊「Create API key」按鈕（或選擇現有的 Google Cloud 專案）

**第五步**：等待幾秒後，您會看到專屬的 API Key，點擊「Copy」複製

🎉 **完成！** 您現在擁有免費的 Gemini API 了

#### Google Gemini 免費額度

| 項目 | 免費額度 |
|------|---------|
| 每分鐘請求數 (RPM) | 15 次 |
| 每日請求數 (RPD) | 1,500 次 |
| 每分鐘 Token 數 (TPM) | 1,000,000 個 |

#### 確認使用的是免費額度

在 Google AI Studio 的 API Key 介面中，確認該 API Key 的 Plan 顯示為 **「Free tier」** 或 **「Unavailable」**，就代表使用的是免費額度，不會被扣款。

詳細圖文教學請參考：[手把手教你申請免費 Google Gemini API](https://lifecheatslab.com/freegeminiapi/)

---

### API 方案比較

| 比較項目 | Azure OpenAI | Google AI Studio |
|---------|-------------|------------------|
| 費用 | 需綁信用卡（$200 免費額度） | 完全免費 |
| 申請難度 | 較複雜 | 非常簡單 |
| 帳號限制 | 必須全新帳號 | 無限制 |
| 設定時間 | 15-30 分鐘 | 5 分鐘 |
| 模型 | GPT 模型 | Gemini 模型 |
| Embeddings | 需額外部署 | 內建免費模型 |

---

## 🗄️ Qdrant 向量資料庫設定

本章節需要使用 Qdrant 向量資料庫來儲存文件的向量嵌入。以下提供兩種設定方式：

### 方案一：Qdrant Cloud（✨ 推薦新手）

**優點**：
- ✅ 完全免費的入門方案（1GB 儲存空間）
- ✅ 無需安裝和維護
- ✅ 3 分鐘完成設定
- ✅ 提供 HTTPS 連線和 API Key 認證

#### Qdrant Cloud 申請步驟

**第一步**：前往 [Qdrant Cloud](https://cloud.qdrant.io/)，點擊「Sign Up」註冊

**第二步**：使用 Google、GitHub 或 Email 註冊帳號

**第三步**：登入後，點擊「Create Cluster」建立叢集

**第四步**：選擇「Free」方案，選擇地區（建議選擇 `aws-us-east-1`）

**第五步**：等待叢集建立完成（約 1-2 分鐘）

**第六步**：點擊叢集名稱，複製「Cluster URL」和「API Key」

🎉 **完成！** 您現在擁有免費的 Qdrant 雲端資料庫

---

### 方案二：本地 Docker 部署

如果您熟悉 Docker，可以在本機運行 Qdrant：

```bash
# 使用 Docker 啟動 Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Qdrant URL 會是: http://localhost:6333
# 本地部署不需要 API Key
```

**本地部署的 .env 設定：**
```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # 留空或不設定
```

---

## 環境需求

- Python 3.11+
- Poetry（套件管理工具）
- Qdrant 向量資料庫（雲端或本地）

## 安裝 Poetry

### macOS / Linux

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Windows (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

安裝完成後，請重新啟動終端機。

## 初始化專案環境

### macOS / Linux

```bash
# 進入 CH6/ch6 目錄（從專案根目錄）
cd python_langchain_gemini_azure/CH6/ch6

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

### Windows

```powershell
# 進入 CH6/ch6 目錄（從專案根目錄）
cd python_langchain_gemini_azure\CH6\ch6

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

## 為什麼使用 langchain-google-genai < 3.0.0？

由於當前專案使用的 `langchain-community 0.3.x` 與 `langchain-google-genai 3.0.0` 存在依賴衝突：

- `langchain-google-genai 3.0.0` 需要 `langchain-core >= 1.0.0`
- `langchain-community 0.3.x` 需要 `langchain-core < 1.0.0`

因此我們使用 **2.x 版本**的 `langchain-google-genai`，這個版本與現有依賴完全相容，並且支援所有 Gemini 模型功能。

## 設定環境變數

在 `CH6/ch6` 目錄的**上一層**（即 `python_langchain_gemini_azure/CH6`）建立 `.env` 檔案：

### 使用 Google Gemini（推薦）

```env
# Google Gemini API
GOOGLE_API_KEY=你的_Google_API_Key
GEMINI_MODEL_ID=gemini-1.5-flash-latest

# Qdrant 向量資料庫
QDRANT_URL=你的_Qdrant_URL
QDRANT_API_KEY=你的_Qdrant_API_Key
```

**範例（使用 Qdrant Cloud）：**
```env
GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL_ID=gemini-1.5-flash-latest
QDRANT_URL=https://xxxxx-xxxxx.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key-here
```

### 使用 Azure OpenAI

```env
# Azure OpenAI
AOAI_API_KEY=你的_Azure_OpenAI_API_Key
AOAI_ENDPOINT=你的_Azure_OpenAI_Endpoint
AOAI_EMBED_DEPLOYMENT_NAME=你的_Embedding_部署名稱
AOAI_GPT_DEPLOYMENT_NAME=你的_GPT_部署名稱

# Qdrant 向量資料庫
QDRANT_URL=你的_Qdrant_URL
QDRANT_API_KEY=你的_Qdrant_API_Key
```

**範例：**
```env
AOAI_API_KEY=1234567890abcdef1234567890abcdef
AOAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AOAI_EMBED_DEPLOYMENT_NAME=text-embedding-ada-002
AOAI_GPT_DEPLOYMENT_NAME=gpt-4
QDRANT_URL=https://xxxxx-xxxxx.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key-here
```

**⚠️ 重要提醒：**
- `.env` 檔案應該放在 `python_langchain_gemini_azure/CH6/` 目錄
- 不要將 `.env` 檔案提交到 Git（應該加入 `.gitignore`）
- 確認 API Key 沒有多餘的空格或引號

---

## 📁 檔案清單

### 01_rag_with_history.py
**Azure OpenAI 版本的 RAG with History 實現**

#### 功能說明：
此程式展示如何使用 Azure OpenAI 建立一個具有對話記憶功能的 RAG 系統。

#### 主要特色：
- ✅ **網頁資料載入**：使用 `WebBaseLoader` 從指定網站載入書籍資訊
- ✅ **文件分割**：使用 `RecursiveCharacterTextSplitter` 將長文件切分成適合處理的片段
- ✅ **向量儲存**：整合 Qdrant 向量資料庫進行高效的語義檢索
- ✅ **對話記憶**：使用 SQLite 資料庫持久化儲存對話歷史
- ✅ **上下文感知**：能夠理解先前的對話內容並做出相應回應

#### 使用的模型：
- **Chat Model**: Azure OpenAI GPT 模型
- **Embeddings**: Azure OpenAI Embeddings 模型

#### 核心流程：
1. 從網頁載入「極速ChatGPT開發者兵器指南」書籍資訊
2. 將文件分割並轉換為向量嵌入
3. 儲存向量到 Qdrant 資料庫
4. 建立檢索鏈與對話記憶系統
5. 執行兩個問題示範對話記憶功能

#### 執行範例：

---

### 01_rag_with_history_gemini.py
**Google Gemini 版本的 RAG with History 實現**

#### 功能說明：
此程式是 `01_rag_with_history.py` 的 Google Gemini 版本，功能完全相同，但使用 Google Gemini 模型替代 Azure OpenAI。

#### 主要特色：
- ✅ **網頁資料載入**：使用 `WebBaseLoader` 從指定網站載入書籍資訊
- ✅ **文件分割**：使用 `RecursiveCharacterTextSplitter` 將長文件切分成適合處理的片段
- ✅ **向量儲存**：整合 Qdrant 向量資料庫進行高效的語義檢索
- ✅ **對話記憶**：使用 SQLite 資料庫持久化儲存對話歷史
- ✅ **上下文感知**：能夠理解先前的對話內容並做出相應回應

#### 使用的模型：
- **Chat Model**: Google Gemini 模型（如 gemini-1.5-flash, gemini-1.5-pro）
- **Embeddings**: Google Gemini Embedding 模型（gemini-embedding-001）

#### 核心流程：
1. 從網頁載入「極速ChatGPT開發者兵器指南」書籍資訊
2. 將文件分割並使用 Gemini Embeddings 轉換為向量
3. 儲存向量到 Qdrant 資料庫
4. 建立檢索鏈與對話記憶系統
5. 執行兩個問題示範對話記憶功能

#### 執行範例：
```bash
# 執行程式
poetry run python ch6/01_rag_with_history_gemini.py
```

---

## 🎯 核心概念

### RAG (Retrieval-Augmented Generation)
RAG 是一種結合資訊檢索與生成模型的技術：

1. **檢索階段**：從向量資料庫中找出與問題相關的文件片段
2. **生成階段**：將檢索到的資訊作為上下文，讓 LLM 生成回答

**優勢：**
- ✅ 提供事實依據，減少幻覺（Hallucination）
- ✅ 可以處理大量文件，不受 LLM 上下文長度限制
- ✅ 資料更新時只需更新向量資料庫，無需重新訓練模型

### 對話記憶 (Chat History)
使用 `SQLChatMessageHistory` 將對話歷史儲存到 SQLite 資料庫：

- **會話管理**：支援多個會話（session）管理
- **持久化儲存**：程式重啟後仍可保留歷史
- **上下文理解**：讓 AI 能夠理解上下文，回答如「我剛剛的問題是什麼」這類問題

**實作細節：**
```python
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///./langchain.db")

chain_with_history = RunnableWithMessageHistory(
    retrieval_chain,
    get_session_history,
    input_messages_key="input",
    output_messages_key="answer",
    history_messages_key="history",
)
```

### 向量資料庫 (Qdrant)
使用 Qdrant 進行高效的向量相似度搜尋：

- **大規模檢索**：支援百萬級向量的快速搜尋
- **部署彈性**：提供雲端和本地部署選項
- **高效演算法**：使用 HNSW（Hierarchical Navigable Small World）演算法
- **過濾功能**：支援結合向量相似度和元資料過濾

### 文件分割 (Document Splitting)
使用 `RecursiveCharacterTextSplitter` 將長文件切分：

```python
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
```

**為什麼需要分割？**
- LLM 有上下文長度限制
- 較小的片段能提供更精確的檢索結果
- 降低處理成本

---

## 📊 執行結果示例

程式會執行兩個問題來展示對話記憶功能：

**第一個問題：**
```
Q: 請問這本書的作者？
A: 這本書的作者是黃建庭(Ryan)及黃兆鴻(Nick)。
```

**第二個問題（展示對話記憶）：**
```
Q: 我剛剛的問題是什麼
A: 您剛剛的問題是「請問這本書的作者？」
```

第二個問題的回答證明了系統能夠記住先前的對話內容！

---

## 🚀 快速開始指南

### Step 1: 安裝依賴

```bash
# 進入專案目錄
cd python_langchain_gemini_azure/CH6/ch6

# 安裝依賴
poetry install

# 安裝 Gemini 支援（如果使用 Gemini 版本）
poetry add "langchain-google-genai<3.0.0"
```

### Step 2: 設定環境變數

在 `CH6` 目錄建立 `.env` 檔案（參考上方環境變數設定章節）

### Step 3: 設定 Qdrant

選擇以下其中一種方式：
- 使用 Qdrant Cloud（推薦）
- 本地 Docker 部署

### Step 4: 執行程式

```bash
# 執行 Gemini 版本（推薦）
poetry run python ch6/01_rag_with_history_gemini.py

# 或執行 Azure OpenAI 版本
poetry run python ch6/01_rag_with_history.py
```

---

## 🐛 常見問題排除

### 問題 1: 找不到 .env 檔案

**錯誤訊息：**
```
KeyError: 'GOOGLE_API_KEY'
```

**解決方法：**
確認 `.env` 檔案位置在 `python_langchain_gemini_azure`，而不是 `CH6/ch6/.env`

### 問題 2: Qdrant 連線失敗

**錯誤訊息：**
```
Connection refused
```

**解決方法：**
- 檢查 `QDRANT_URL` 格式是否正確
- 確認 Qdrant Cloud 叢集狀態為「Running」
- 檢查 `QDRANT_API_KEY` 是否正確

### 問題 3: 依賴衝突

**錯誤訊息：**
```
langchain-core version conflict
```

**解決方法：**
使用 `langchain-google-genai<3.0.0` 版本：
```bash
poetry add "langchain-google-genai<3.0.0"
```

### 問題 4: 網頁載入失敗

**錯誤訊息：**
```
Failed to load URL
```

**解決方法：**
- 檢查網路連線
- 確認目標網站 `https://www.drmaster.com.tw/bookinfo.asp?BookID=MP22359` 是否可訪問
- 可能需要設定代理伺服器

---

## 📚 延伸學習

### 進階主題

1. **向量資料庫優化**
   - 調整 chunk size、overlap 等參數
   - 使用不同的分割策略（依段落、依語意）
   - 嘗試不同的 Embeddings 模型

2. **檢索策略**
   - MMR（Maximal Marginal Relevance）：提高檢索多樣性
   - Similarity Score Threshold：設定相似度門檻
   - Contextual Compression：壓縮檢索結果

3. **記憶管理**
   - 記憶摘要：自動摘要長對話
   - 記憶裁剪：只保留最近 N 輪對話
   - 混合記憶：結合短期和長期記憶

4. **多輪對話**
   - 建立更複雜的對話流程
   - 實作對話分支
   - 加入使用者意圖識別

---

## 🔗 參考資料

### 官方文檔
- [LangChain 官方文檔](https://python.langchain.com/)
- [Qdrant 官方文檔](https://qdrant.tech/)
- [Google Gemini API 文檔](https://ai.google.dev/)
- [Azure OpenAI 文檔](https://learn.microsoft.com/azure/ai-services/openai/)

### 教學資源
- 書籍資料來源：[極速ChatGPT開發者兵器指南](https://www.drmaster.com.tw/bookinfo.asp?BookID=MP22359)
- [RAG 技術介紹](https://python.langchain.com/docs/use_cases/question_answering/)
- [對話記憶管理](https://python.langchain.com/docs/modules/memory/)

### 相關工具
- [Poetry 文檔](https://python-poetry.org/docs/)
- [BeautifulSoup 文檔](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

## 💡 實用提示

### 效能優化
- 首次執行時，程式會重新建立向量資料庫（`force_recreate=True`）
- 之後可以將 `force_recreate` 改為 `False` 以節省時間
- 對話歷史儲存在 `langchain.db` SQLite 資料庫中
- 不同的 `session_id` 可以管理不同的對話會話

### 開發建議
- 建議先測試 Qdrant 連線是否正常，再執行完整程式
- 可以先用少量文件測試，確認流程正常後再處理大量資料
- 開發時可以啟用 `verbose=True` 查看詳細執行過程

