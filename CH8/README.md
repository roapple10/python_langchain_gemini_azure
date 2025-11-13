# CH8: 多模態 AI 應用

本章節展示如何使用 LangChain 和 Google Gemini 進行多模態 AI 應用開發，包括文字、圖片、音訊和影片的處理與分析。

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
5. 取得 Endpoint 和 API Key

詳細教學請參考：[Azure OpenAI Service 申請教學](https://ithelp.ithome.com.tw/m/articles/10353046)

**如果您不符合全新帳號條件，請改用下方推薦的 Google AI Studio**

---

### 方案二：Google AI Studio API

**為什麼推薦使用 Google AI Studio？**

✅ **完全免費**：無需綁定信用卡  
✅ **設定簡單**：5 分鐘內完成申請  
✅ **無帳號限制**：任何 Google 帳號都能使用  
✅ **慷慨的免費額度**：每分鐘 15 個請求，足夠學習使用  
✅ **強大的 Gemini 模型**：效能媲美 GPT-4，支援多模態輸入（文字、圖片、音訊、影片）

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
| 帳號限制 | 必須全新帳號 | 較無限制 |
| 設定時間 | 1-3 分鐘 | 1-3 分鐘 |
| 模型 | GPT 模型 | Gemini 模型 |
| 多模態支援 | 有限 | 完整支援（文字、圖片、音訊、影片） |

---

## 環境需求

- Python 3.11+
- Poetry（套件管理工具）或 Python venv

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

### 方法一：使用 Poetry（推薦）

#### macOS / Linux

```bash
# 進入 CH8 目錄（從專案根目錄）
cd python_langchain_gemini_azure/CH8

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

#### Windows

```powershell
# 進入 CH8 目錄（從專案根目錄）
cd python_langchain_gemini_azure\CH8

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

### 方法二：使用 Python venv

#### macOS / Linux

```bash
# 進入 CH8 目錄
cd python_langchain_gemini_azure/CH8

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 升級 pip
pip install --upgrade pip

# 安裝依賴
pip install -r requirements.txt
```

#### Windows (PowerShell)

```powershell
# 進入 CH8 目錄
cd python_langchain_gemini_azure\CH8

# 建立虛擬環境
python -m venv venv

# 修改執行原則（僅需執行一次，如果遇到執行原則錯誤）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 升級 pip
pip install --upgrade pip

# 安裝依賴
pip install -r requirements.txt
```

詳細的 venv 設定教學請參考：[venv_setup.md](./venv_setup.md)

## 為什麼使用 langchain-google-genai < 3.0.0？

由於當前專案使用的 `langchain-community 0.3.x` 與 `langchain-google-genai 3.0.0` 存在依賴衝突：

- `langchain-google-genai 3.0.0` 需要 `langchain-core >= 1.0.0`
- `langchain-community 0.3.x` 需要 `langchain-core < 1.0.0`

因此我們使用 **2.x 版本**的 `langchain-google-genai`，這個版本與現有依賴完全相容，並且支援所有 Gemini 模型功能。

## 設定環境變數

在專案根目錄建立 `.env` 檔案（Mac 和 Windows 相同）：

```env
# Google Gemini API Key（用於所有範例）
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL_ID=gemini-1.5-flash-latest
```

### 取得 API Keys

- **Google Gemini**: https://ai.google.dev/（推薦使用，免費且無需信用卡）

## 執行範例程式

### 使用 Poetry

#### macOS / Linux

```bash
# 8-2: 基本文字生成
poetry run python 8-2/app.py

# 8-3: 圖片識別（使用 LangChain）
poetry run python 8-3/app.py

# 8-4: 音訊處理
poetry run python 8-4/app.py

# 8-5: 音訊處理（與 8-4 類似）
poetry run python 8-5/app.py

# 8-6: 影片和圖片的多模態處理
poetry run python 8-6/app.py
```

#### Windows

```powershell
# 8-2: 基本文字生成
poetry run python 8-2/app.py

# 8-3: 圖片識別（使用 LangChain）
poetry run python 8-3/app.py

# 8-4: 音訊處理
poetry run python 8-4/app.py

# 8-5: 音訊處理（與 8-4 類似）
poetry run python 8-5/app.py

# 8-6: 影片和圖片的多模態處理
poetry run python 8-6/app.py
```

### 使用 venv

#### macOS / Linux

```bash
# 啟動虛擬環境
source venv/bin/activate

# 8-2: 基本文字生成
python 8-2/app.py

# 8-3: 圖片識別（使用 LangChain）
python 8-3/app.py

# 8-4: 音訊處理
python 8-4/app.py

# 8-5: 音訊處理（與 8-4 類似）
python 8-5/app.py

# 8-6: 影片和圖片的多模態處理
python 8-6/app.py

# 離開虛擬環境
deactivate
```

#### Windows (PowerShell)

```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 8-2: 基本文字生成
python 8-2/app.py

# 8-3: 圖片識別（使用 LangChain）
python 8-3/app.py

# 8-4: 音訊處理
python 8-4/app.py

# 8-5: 音訊處理（與 8-4 類似）
python 8-5/app.py

# 8-6: 影片和圖片的多模態處理
python 8-6/app.py

# 離開虛擬環境
deactivate
```

## 啟用虛擬環境（進階）

如果您想要直接在虛擬環境中工作：

### macOS / Linux（Poetry）

```bash
### 啟動虛擬環境（Poetry 2.0+）

**重要提示：** 從 Poetry 2.0.0 開始，`poetry shell` 命令不再預設可用。請使用以下新方法：

#### 方法 1：使用 `env activate` 命令（官方推薦）

**步驟 1：** 執行以下命令查看啟動環境的指令：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry env activate
```


# 現在可以直接執行 Python 腳本
python 8-2/app.py
python 8-3/app.py
python 8-4/app.py
python 8-5/app.py
python 8-6/app.py

# 離開虛擬環境
exit
```

### Windows（Poetry）

```powershell
# 啟用虛擬環境
poetry shell

# 現在可以直接執行 Python 腳本
python 8-2/app.py
python 8-3/app.py
python 8-4/app.py
python 8-5/app.py
python 8-6/app.py

# 離開虛擬環境
exit
```

## 章節說明

### 8-2: 基本文字生成
- `app.py`: 使用 Google Gemini 進行基本文字生成
- **學習重點**：了解如何使用 Google Generative AI SDK 進行簡單的文字生成任務

### 8-3: 圖片識別
- `app.py`: 使用 LangChain 和 Google Gemini 進行圖片識別
- **學習重點**：
  - 如何使用 LangChain 的 `ChatGoogleGenerativeAI` 處理圖片輸入
  - 多模態訊息的組合方式（文字 + 圖片）
  - 使用 `HumanMessage` 傳遞包含圖片 URL 的內容

### 8-4: 音訊處理
- `app.py`: 使用 Google Generative AI SDK 處理音訊檔案
- **學習重點**：
  - 如何上傳音訊檔案到 Google AI
  - 使用 Gemini 模型分析音訊內容
  - 檔案上傳與管理的流程

### 8-5: 音訊處理（進階）
- `app.py`: 音訊處理的進階範例
- **學習重點**：
  - 與 8-4 類似的功能，但展示不同的使用方式
  - 系統指令（system instruction）的設定
  - 檔案清理的最佳實踐

### 8-6: 影片和圖片的多模態處理
- `app.py`: 同時處理影片和圖片的多模態應用
- **學習重點**：
  - 如何上傳和處理影片檔案
  - 等待影片處理完成的機制
  - 同時使用多種媒體類型（文字、圖片、影片）進行分析
  - 影片中的人物識別和時間定位
  - 多模態輸入的組合方式

