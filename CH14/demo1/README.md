# CH14 Demo1 環境設定指南

本文件說明如何建立並啟動 Python virtual environment (venv) 來執行此專案。本專案展示如何使用 LangGraph 和 Google Gemini 建立智能 Agent 系統，實現酒店訂房服務的自動化處理。

## 前置需求

- Python 3.11 或以上版本
- pip (Python 套件管理工具)

## 建立 Virtual Environment

### 步驟 1: 進入專案目錄

```bash
cd python_langchain_gemini_azure/CH14
```

### 步驟 2: 建立 Virtual Environment

使用以下指令建立虛擬環境：

```bash
python -m venv venv
```

這會在當前目錄下建立一個名為 `venv` 的虛擬環境資料夾。

## 啟動 Virtual Environment

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```powershell
# 修改執行原則（僅需執行一次，如果遇到執行原則錯誤）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 升級 pip
pip install --upgrade pip

# 安裝依賴
pip install -r requirements.txt
```

啟動成功後，終端機提示字元前會顯示 `(venv)`，表示虛擬環境已啟動。

## 安裝專案依賴

### 方法 1: 使用 requirements.txt (推薦)

如果專案有 `requirements.txt` 檔案，使用以下指令安裝：

```bash
pip install -r requirements.txt
```

### 方法 2: 從 pyproject.toml 安裝

由於此專案使用 Poetry 管理，您可以：

1. 安裝 Poetry（如果尚未安裝）：
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. 使用 Poetry 安裝依賴：
```bash
poetry install
```

3. 或者手動安裝 pyproject.toml 中列出的套件：
```bash
pip install python-dotenv>=1.0.1,<2.0.0
pip install langchain-core==0.3.0
pip install langchain==0.3.0
pip install langchain-community==0.3.0
pip install langchain-google-genai<3.0.0
pip install langgraph>=0.2.14,<0.3.0
```

## 設定環境變數

在專案根目錄（`python_langchain_gemini_azure/`）建立 `.env` 檔案，並填入以下 Google Gemini 相關設定：

```env
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_ID=gemini-1.5-pro
```

**注意事項：**
- `GOOGLE_API_KEY`: 您的 Google API Key，可從 [Google AI Studio](https://makersuite.google.com/app/apikey) 取得
- `GEMINI_MODEL_ID`: 使用的 Gemini 模型名稱，例如 `gemini-1.5-pro` 或 `gemini-1.5-flash`

## 執行專案

本專案包含五個程式，展示 LangGraph Agent 的不同功能與進階應用：

### demo14-1_gemini.py - 基礎 ReAct Agent

**功能說明：**
此程式展示最基本的 LangGraph ReAct Agent 實作，實現酒店訂房查詢功能：

1. **工具定義**：
   - `get_current_date()`: 取得當前日期
   - `check_room_availability(date)`: 查詢指定日期的可用房間
2. **Agent 建立**：使用 `create_react_agent` 建立基本的 ReAct Agent
3. **執行查詢**：處理自然語言查詢「可以預約明天的住宿嗎」，Agent 會自動：
   - 理解查詢意圖
   - 調用 `get_current_date` 取得今天日期
   - 計算明天的日期
   - 調用 `check_room_availability` 查詢可用房間
   - 回覆查詢結果

**執行指令：**
```bash
python demo1/demo1/demo14-1_gemini.py
```

**注意事項：**
- 此程式展示基本的 Agent 運作方式，不包含記憶功能
- 每次查詢都是獨立的，無法記住之前的對話內容

---

### demo14-2_gemini.py - 加入記憶功能的 Agent

**功能說明：**
此程式在基礎 Agent 上加入對話記憶功能，使用 `MemorySaver` 保存對話歷史：

1. **記憶功能**：使用 `MemorySaver` 作為 checkpointer，保存對話狀態
2. **多輪對話**：支援連續對話，Agent 可以記住之前的對話內容
3. **執行範例**：
   - 第一輪：「可以預訂明天住宿嗎」- Agent 查詢並回覆
   - 第二輪：「我剛預訂了什麼時候的房間」- Agent 根據記憶回答

**執行指令：**
```bash
python demo1/demo1/demo14-2_gemini.py
```

**注意事項：**
- 使用 `thread_id` 來區分不同的對話線程
- 記憶保存在記憶體中，程式結束後會消失

---

### demo14-3_gemini.py - 自訂提示詞的 Agent

**功能說明：**
此程式展示如何透過 `state_modifier` 參數自訂 Agent 的行為和回應風格：

1. **自訂提示詞**：設定 Agent 為「酒店訂房機器人」，要求同時回應繁體中文和英文
2. **行為調整**：透過提示詞改變 Agent 的回應方式和語言風格
3. **功能保留**：保留記憶功能和所有工具功能

**執行指令：**
```bash
python demo1/demo1/demo14-3_gemini.py
```

**注意事項：**
- 可以透過修改 `agent_prompt` 來調整 Agent 的行為
- 提示詞會影響 Agent 的決策和回應風格

---

### demo14-4_gemini.py - 進階 Agent（含客戶服務鏈）

**功能說明：**
此程式展示最完整的 Agent 實作，包含額外的工具和更複雜的處理流程：

1. **新增工具**：
   - `get_customer_service_chain(input)`: 處理客戶評論，分析情感並生成回應
2. **工具鏈整合**：客戶服務工具內部使用 LangChain Chain 來處理複雜邏輯
3. **多樣化查詢**：支援訂房查詢、記憶查詢和客戶評論處理

**執行範例**：
- 訂房查詢：「可以預訂明天住宿嗎」
- 記憶查詢：「我剛預訂了什麼時候的房間」
- 客戶評論：「你們的服務真的很是太棒了！」- Agent 會分析情感並回應

**執行指令：**
```bash
python demo1/demo1/demo14-4_gemini.py
```

**注意事項：**
- 此程式展示如何整合 LangChain Chain 作為 Agent 的工具
- 客戶服務工具內部使用 LLM 來分析情感並生成回應

---

### demo14-5_gemini.py - 互動式 Agent 系統

**功能說明：**
此程式是完整的互動式 Agent 系統，結合了所有先前程式的功能，並提供持續的對話介面：

1. **完整功能整合**：
   - 包含所有工具（日期查詢、房間查詢、客戶服務）
   - 記憶功能（MemorySaver）
   - 自訂提示詞（雙語回應）
2. **互動式介面**：提供持續的對話循環，允許用戶多次提問
3. **示例提示**：程式啟動時顯示可用的查詢範例
4. **退出機制**：支援 `quit`、`exit`、`退出`、`結束` 等指令來結束程式

**執行範例**：
程式會顯示以下示例輸入：
- 「可以預訂明天住宿嗎」
- 「我剛預訂了什麼時候的房間」
- 「你們的服務真的很是太棒了！」
- 「查詢 2025/12/01 的可用房間」
- 「今天的日期是什麼？」

用戶可以持續輸入問題，Agent 會根據對話歷史和工具來回應。

**執行指令：**
```bash
python demo1/demo1/demo14-5_gemini.py
```

**注意事項：**
- 此程式適合實際測試和演示 Agent 的完整功能
- 所有對話都會保存在記憶中，Agent 可以記住之前的對話內容
- 輸入空行會被忽略，可以繼續輸入
- 使用 `quit` 或 `exit` 可以正常結束程式

---

### 執行順序

建議按照以下順序執行，逐步了解 LangGraph Agent 的功能：

1. **基礎學習**：先執行 `demo14-1_gemini.py` 了解基本 Agent 運作
2. **記憶功能**：執行 `demo14-2_gemini.py` 學習如何加入對話記憶
3. **自訂行為**：執行 `demo14-3_gemini.py` 學習如何自訂 Agent 提示詞
4. **進階應用**：執行 `demo14-4_gemini.py` 學習如何整合複雜工具和 Chain
5. **互動體驗**：執行 `demo14-5_gemini.py` 體驗完整的互動式 Agent 系統

## 停用 Virtual Environment

當您完成工作後，可以使用以下指令停用虛擬環境：

```bash
deactivate
```

## 注意事項

1. 每次開啟新的終端機視窗時，都需要重新啟動虛擬環境
2. 確保已正確設定 `.env` 檔案中的 `GOOGLE_API_KEY` 和 `GEMINI_MODEL_ID`
3. 本專案使用 Google Gemini API，需要有效的 API Key 才能執行
4. 程式中的房間資料是模擬資料，實際應用時應連接真實的資料庫或 API
5. 記憶功能使用記憶體儲存，程式結束後對話記錄會消失

## 疑難排解

### 問題：找不到 python3 指令

**解決方案：**
- macOS/Linux: 嘗試使用 `python` 替代 `python3`
- Windows: 使用 `py` 指令或確保 Python 已加入系統 PATH

### 問題：pip 安裝套件時出現權限錯誤

**解決方案：**
- 確保已啟動虛擬環境
- 不要使用 `sudo`，虛擬環境不需要系統權限

### 問題：虛擬環境啟動後仍使用系統 Python

**解決方案：**
- 確認啟動指令正確執行
- 檢查終端機提示字元是否顯示 `(venv)`
- 使用 `which python` (macOS/Linux) 或 `where python` (Windows) 確認使用的 Python 路徑

