# CH10 Demo1 環境設定指南

本文件說明如何建立並啟動 Python virtual environment (venv) 來執行此專案。

## 前置需求

- Python 3.11 或以上版本
- pip (Python 套件管理工具)

## 建立 Virtual Environment

### 步驟 1: 進入專案目錄

```bash
cd python_langchain_gemini_azure/CH10
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

```bash
venv\Scripts\activate
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
pip install langchain==^0.3.0
pip install python-dotenv==^1.0.1
pip install langchain-openai==^0.2.0
pip install langchain-community==^0.3.0
pip install pypdf==^4.3.1
pip install langchain-qdrant==0.2.0.dev1
pip install qdrant-client
```

## 設定環境變數

在專案根目錄建立 `.env` 檔案，並填入以下 Azure OpenAI 相關設定：

## 執行專案

本專案包含兩個程式，分別用於不同的階段：

### demo10-1_gemini.py - 文件向量化與入庫

**功能說明：**
此程式用於**第一次**將知識文件（PDF）載入到 Qdrant 向量資料庫。主要執行以下步驟：

1. **載入 PDF 文件**：使用 `PyPDFLoader` 載入 `docs/勞動基準法.pdf` 文件
2. **文本分割**：使用 `RecursiveCharacterTextSplitter` 將文件分割成小塊（chunk_size=1000, chunk_overlap=200）
3. **向量化與儲存**：使用 Google Gemini Embeddings 將文本轉換為向量，並存入 Qdrant 向量資料庫的 `km_docs` collection
4. **初始化完成**：完成後，向量資料庫中已包含文件的向量表示，可供後續查詢使用

**執行時機：**
- 首次執行專案時
- 需要更新或重新載入文件時
- 需要建立新的向量資料庫 collection 時

**執行指令：**
```bash
python demo1/demo1/demo10-1_gemini.py
```

**注意事項：**
- 執行此程式前，請確保 PDF 文件位於 `demo1/docs/勞動基準法.pdf`
- 程式執行時會將文件載入並向量化，可能需要一些時間
- 查詢相關的程式碼在此程式中被註解，因為此階段主要用於資料準備

---

### demo10-2_gemini.py - RAG 問答查詢

**功能說明：**
此程式用於**後續查詢**，當向量資料已經存在於 Qdrant 時使用。實現完整的 RAG (Retrieval-Augmented Generation) 問答流程：

1. **連接向量資料庫**：連接到已存在的 Qdrant 向量資料庫和 `km_docs` collection
2. **設置檢索器**：建立檢索器（Retriever），設定檢索前 3 個最相似的文檔片段
3. **建立 QA Chain**：組合檢索、提示模板、語言模型和輸出解析器，建立完整的問答鏈
4. **執行查詢**：輸入問題「勞工加班費的計算方式是什麼？」，系統會：
   - 從向量資料庫中檢索相關文檔片段
   - 將檢索到的上下文與問題一起送入 Gemini 模型
   - 生成基於參考資料的專業回答
5. **輸出結果**：在終端機顯示 AI 生成的回答

**執行時機：**
- 完成 `demo10-1_gemini.py` 後
- 需要對已載入的文件進行問答查詢時
- 測試 RAG 系統功能時

**執行指令：**
```bash
python demo1/demo1/demo10-2_gemini.py
```

**注意事項：**
- 執行此程式前，必須先執行 `demo10-1_gemini.py` 完成文件載入
- 文件載入相關的程式碼在此程式中被註解，因為向量資料已存在
- 可以修改程式中的問題來測試不同的查詢

---

### 執行順序

建議按照以下順序執行：

1. **首次執行**：先執行 `demo10-1_gemini.py` 完成文件載入
2. **後續查詢**：執行 `demo10-2_gemini.py` 進行問答查詢
3. **重複查詢**：之後可以多次執行 `demo10-2_gemini.py` 進行不同問題的查詢，無需重複執行 `demo10-1_gemini.py`

## 停用 Virtual Environment

當您完成工作後，可以使用以下指令停用虛擬環境：

```bash
deactivate
```

## 注意事項

1. 每次開啟新的終端機視窗時，都需要重新啟動虛擬環境
2. 確保在執行專案前，Qdrant 向量資料庫服務已啟動（預設在 `http://localhost:6333`）
3. 首次執行時，需要先將 PDF 文件載入到 Qdrant（請參考程式碼中的註解說明）

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

