# CH5: LangChain Runnable 與 LCEL 表達式

本章節深入探討 LangChain 的核心架構 - **Runnable 物件**與 **LCEL（LangChain Expression Language）表達式**。學習如何使用 LangChain 的現代化 API 來建立各種工作流程，包括順序執行、並行處理、條件分支、容錯機制等進階應用。

## 🎯 本章學習目標

- ✅ 理解 Runnable 物件的核心概念
- ✅ 掌握 LCEL 表達式的使用方式
- ✅ 學習 RunnableSequence（順序執行）
- ✅ 學習 RunnableParallel（並行處理）
- ✅ 學習 RunnableBranch（條件分支）
- ✅ 學習 RunnableLambda（自訂函數）
- ✅ 學習 RunnableWithFallbacks（容錯機制）
- ✅ 學習 RunnablePassthrough（資料傳遞）

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

### 方案二：Google AI Studio API（✨ 推薦）

**為什麼推薦使用 Google AI Studio？**

✅ **完全免費**：無需綁定信用卡  
✅ **設定簡單**：5 分鐘內完成申請  
✅ **無帳號限制**：任何 Google 帳號都能使用  
✅ **慷慨的免費額度**：每分鐘 15 個請求，足夠學習使用  
✅ **強大的 Gemini 模型**：效能媲美 GPT-4

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

---

## 環境需求

- Python 3.11+
- Poetry（套件管理工具）

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
# 進入 CH5/demo1 目錄（從專案根目錄）
cd python_langchain_gemini_azure/CH5/demo1

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

### Windows

```powershell
# 進入 CH5/demo1 目錄（從專案根目錄）
cd python_langchain_gemini_azure\CH5\demo1

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

在專案根目錄建立 `.env` 檔案（Mac 和 Windows 相同）：

```env
# Azure OpenAI 設定（用於 demo5-1.py 到 demo5-8.py）
AZURE_OPENAI_ENDPOINT=your-azure-endpoint-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name-here
AZURE_OPENAI_Base_DEPLOYMENT_NAME=your-base-deployment-name-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_KEY=your-azure-api-key-here

# Google Gemini API Key（用於 demo5-1_gemini.py 到 demo5-8_gemini.py）
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL_ID=gemini-1.5-flash-latest
```

### 取得 API Keys

- **Azure OpenAI**: https://portal.azure.com/（需要建立 Azure OpenAI 資源）
- **Google Gemini**: https://ai.google.dev/（推薦使用，免費且無需信用卡）

## 執行範例程式

### macOS / Linux

```bash
# demo5-1: RunnableSequence（順序工作流程）
poetry run python demo1/demo5-1.py          # Azure OpenAI 版本
poetry run python demo1/demo5-1_gemini.py   # Google Gemini 版本

# demo5-2: RunnableParallel（文本分析）
poetry run python demo1/demo5-2.py          # Azure OpenAI 版本
poetry run python demo1/demo5-2_gemini.py   # Google Gemini 版本

# demo5-3: RunnableParallel（多語言翻譯）
poetry run python demo1/demo5-3.py          # Azure OpenAI 版本
poetry run python demo1/demo5-3_gemini.py   # Google Gemini 版本

# demo5-4: RunnableBranch（語言識別分支）
poetry run python demo1/demo5-4.py          # Azure OpenAI 版本
poetry run python demo1/demo5-4_gemini.py   # Google Gemini 版本

# demo5-5: RunnableLambda（訂單處理）
poetry run python demo1/demo5-5.py          # Azure OpenAI 版本
poetry run python demo1/demo5-5_gemini.py   # Google Gemini 版本

# demo5-6: RunnableWithFallbacks（容錯機制）
poetry run python demo1/demo5-6.py          # Azure OpenAI 版本
poetry run python demo1/demo5-6_gemini.py   # Google Gemini 版本

# demo5-7: RunnablePassthrough（對聯生成）
poetry run python demo1/demo5-7.py          # Azure OpenAI 版本
poetry run python demo1/demo5-7_gemini.py   # Google Gemini 版本

# demo5-8: RunnablePassthrough（對聯生成與分析）
poetry run python demo1/demo5-8.py          # Azure OpenAI 版本
poetry run python demo1/demo5-8_gemini.py   # Google Gemini 版本
```

### Windows

```powershell
# demo5-1: RunnableSequence（順序工作流程）
poetry run python demo1/demo5-1.py          # Azure OpenAI 版本
poetry run python demo1/demo5-1_gemini.py   # Google Gemini 版本

# demo5-2: RunnableParallel（文本分析）
poetry run python demo1/demo5-2.py          # Azure OpenAI 版本
poetry run python demo1/demo5-2_gemini.py   # Google Gemini 版本

# demo5-3: RunnableParallel（多語言翻譯）
poetry run python demo1/demo5-3.py          # Azure OpenAI 版本
poetry run python demo1/demo5-3_gemini.py   # Google Gemini 版本

# demo5-4: RunnableBranch（語言識別分支）
poetry run python demo1/demo5-4.py          # Azure OpenAI 版本
poetry run python demo1/demo5-4_gemini.py   # Google Gemini 版本

# demo5-5: RunnableLambda（訂單處理）
poetry run python demo1/demo5-5.py          # Azure OpenAI 版本
poetry run python demo1/demo5-5_gemini.py   # Google Gemini 版本

# demo5-6: RunnableWithFallbacks（容錯機制）
poetry run python demo1/demo5-6.py          # Azure OpenAI 版本
poetry run python demo1/demo5-6_gemini.py   # Google Gemini 版本

# demo5-7: RunnablePassthrough（對聯生成）
poetry run python demo1/demo5-7.py          # Azure OpenAI 版本
poetry run python demo1/demo5-7_gemini.py   # Google Gemini 版本

# demo5-8: RunnablePassthrough（對聯生成與分析）
poetry run python demo1/demo5-8.py          # Azure OpenAI 版本
poetry run python demo1/demo5-8_gemini.py   # Google Gemini 版本
```

---

## 📚 範例檔案詳細介紹

### demo5-1: RunnableSequence - 順序工作流程 🔄

**檔案**：
- `demo5-1.py` - Azure OpenAI 版本
- `demo5-1_gemini.py` - Google Gemini 版本

**功能說明**：
展示如何使用 `RunnableSequence` 建立順序執行的工作流程，將多個任務串接起來。

**工作流程**：
1. 第一步：根據主題創作中文短文
2. 第二步：將中文短文翻譯成英文

**學習重點**：
- ✅ 理解 `RunnableSequence` 的基本結構
- ✅ 學習兩種建立方式：
  - 方法 1：`RunnableSequence(step1, step2, step3, ...)`
  - 方法 2：LCEL 表達式 `step1 | step2 | step3`
- ✅ 掌握資料在步驟間的自動傳遞機制
- ✅ 使用 `StrOutputParser()` 解析 LLM 輸出

**執行範例**：
```bash
poetry run python demo1/demo5-1_gemini.py
```

**預期輸出**：
輸入主題「生成式AI的未來」後，會先生成中文文章，然後自動翻譯成英文。

---

### demo5-2: RunnableParallel - 文本分析 ⚡

**檔案**：
- `demo5-2.py` - Azure OpenAI 版本
- `demo5-2_gemini.py` - Google Gemini 版本

**功能說明**：
使用 `RunnableParallel` 同時執行多個分析任務，提升效率。

**並行任務**：
1. **情感分析**：分析文本的情感傾向（正面/負面/中立）
2. **主題提取**：提取文本的主要主題
3. **摘要生成**：生成文本的簡短摘要

**學習重點**：
- ✅ 理解 `RunnableParallel` 的並行處理機制
- ✅ 學習如何將輸入同時發送給多個 chain
- ✅ 掌握結果的字典格式輸出
- ✅ 了解並行處理與順序處理的效能差異

**執行範例**：
```bash
poetry run python demo1/demo5-2_gemini.py
```

**預期輸出**：
```
情感分析: 正面
主題: 飯店住宿體驗
摘要: 作者對飯店的整體評價良好，特別稱讚服務品質...
```

---

### demo5-3: RunnableParallel - 多語言翻譯 🌐

**檔案**：
- `demo5-3.py` - Azure OpenAI 版本
- `demo5-3_gemini.py` - Google Gemini 版本

**功能說明**：
將中文文本同時翻譯成多種語言，展示 `RunnableParallel` 的實用應用。

**翻譯語言**：
1. **英文翻譯**
2. **日文翻譯**
3. **法文翻譯**

**學習重點**：
- ✅ 應用 `RunnableParallel` 解決實際問題
- ✅ 學習多語言處理的工作流程設計
- ✅ 理解如何建立專門的語言專家 chain
- ✅ 掌握並行翻譯的效率優勢

**執行範例**：
```bash
poetry run python demo1/demo5-3_gemini.py
```

**預期輸出**：
輸入中文後，會同時得到英文、日文、法文三種翻譯結果。

---

### demo5-4: RunnableBranch - 語言識別分支 🌿

**檔案**：
- `demo5-4.py` - Azure OpenAI 版本
- `demo5-4_gemini.py` - Google Gemini 版本

**功能說明**：
根據輸入文本的語言自動選擇對應的客服 chain 進行回應。

**分支邏輯**：
1. **語言識別**：判斷輸入是中文、英文還是其他語言
2. **條件分支**：
   - 如果是中文 → 使用中文客服機器人
   - 如果是英文 → 使用英文客服機器人
   - 其他語言 → 預設使用英文客服機器人

**學習重點**：
- ✅ 理解 `RunnableBranch` 的條件分支機制
- ✅ 學習如何定義條件判斷函數
- ✅ 掌握 Lambda 表達式在條件判斷中的應用
- ✅ 了解如何設定預設分支（fallback）
- ✅ 結合 `RunnableSequence` 建立完整工作流程

**執行範例**：
```bash
poetry run python demo1/demo5-4_gemini.py
```

**測試案例**：
程式中提供了三種語言的測試文本（中文、英文、日文），可以看到系統如何自動選擇對應的處理方式。

---

### demo5-5: RunnableLambda - 訂單處理 📦

**檔案**：
- `demo5-5.py` - Azure OpenAI 版本
- `demo5-5_gemini.py` - Google Gemini 版本

**功能說明**：
使用 `RunnableLambda` 包裝自訂 Python 函數，實現訂單驗證與處理流程。

**處理流程**：
1. **訂單驗證**：檢查 customer_id 和商品清單
2. **資料準備**：將訂單資訊轉換為 JSON 格式
3. **LLM 摘要**：使用 LLM 生成訂單摘要或錯誤說明
4. **結果輸出**：輸出處理結果

**學習重點**：
- ✅ 理解 `RunnableLambda` 的作用
- ✅ 學習如何將自訂 Python 函數整合進 LangChain 工作流程
- ✅ 掌握資料驗證的實作方式
- ✅ 了解如何在 Runnable 之間傳遞複雜資料結構
- ✅ 學習使用 `json.dumps()` 處理 JSON 資料

**執行範例**：
```bash
poetry run python demo1/demo5-5_gemini.py
```

**測試案例**：
程式會測試三種訂單：
1. ✅ 有效訂單（有客戶ID，有商品）
2. ❌ 無效訂單（有客戶ID，無商品）
3. ❌ 無效訂單（無客戶ID，有商品）

---

### demo5-6: RunnableWithFallbacks - 容錯機制 🛡️

**檔案**：
- `demo5-6.py` - Azure OpenAI 版本
- `demo5-6_gemini.py` - Google Gemini 版本

**功能說明**：
實作多層容錯機制，當主要服務失敗時自動切換到備用服務。

**容錯層級**：
1. **主要服務**：進階模型（可能不穩定）
2. **第一備援**：基礎模型
3. **第二備援**：預設回應（客服專線訊息）

**學習重點**：
- ✅ 理解 `RunnableWithFallbacks` 的容錯機制
- ✅ 學習如何建立多層備援系統
- ✅ 掌握異常處理與自動切換
- ✅ 了解如何提升系統穩定性
- ✅ 學習模擬服務失敗的測試方法

**執行範例**：
```bash
poetry run python demo1/demo5-6_gemini.py
```

**行為說明**：
程式會執行 5 次測試，觀察當主要服務隨機失敗時，系統如何自動切換到備用服務。

---

### demo5-7: RunnablePassthrough - 對聯生成 🎨

**檔案**：
- `demo5-7.py` - Azure OpenAI 版本
- `demo5-7_gemini.py` - Google Gemini 版本

**功能說明**：
使用 `RunnablePassthrough` 傳遞額外資料（寫作風格範例），實現對聯創作。

**工作流程**：
1. **接收主題**：使用者輸入對聯主題
2. **傳遞範例**：將寫作風格範例傳遞給 LLM
3. **生成對聯**：LLM 參考範例創作對聯

**學習重點**：
- ✅ 理解 `RunnablePassthrough` 的資料傳遞機制
- ✅ 學習如何同時傳遞多個參數給 Prompt
- ✅ 掌握字典解包在 Runnable 中的應用
- ✅ 了解如何提供參考資料給 LLM
- ✅ 學習 Lambda 函數在資料準備中的使用

**執行範例**：
```bash
poetry run python demo1/demo5-7_gemini.py
```

**預期輸出**：
根據主題「生成式AI」，參考提供的古典對聯風格，創作出對仗工整的對聯。

---

### demo5-8: RunnablePassthrough - 對聯生成與分析 📊

**檔案**：
- `demo5-8.py` - Azure OpenAI 版本
- `demo5-8_gemini.py` - Google Gemini 版本

**功能說明**：
在 demo5-7 的基礎上增加對聯分析功能，展示複雜的資料處理流程。

**工作流程**：
1. **接收主題**：使用者輸入對聯主題
2. **傳遞範例**：將寫作風格範例傳遞給 LLM
3. **生成對聯**：LLM 參考範例創作對聯
4. **資料轉換**：將 LLM 輸出轉換為字典格式
5. **分析對聯**：分析字數、重複字元等統計資訊
6. **結果輸出**：輸出對聯內容與分析結果

**學習重點**：
- ✅ 掌握 `RunnablePassthrough.assign()` 的進階用法
- ✅ 學習如何在工作流程中插入自訂分析函數
- ✅ 理解資料在多個 Runnable 間的轉換
- ✅ 了解如何保留原始資料並添加新資料
- ✅ 學習 Lambda 函數在資料處理中的靈活應用

**執行範例**：
```bash
poetry run python demo1/demo5-8_gemini.py
```

**預期輸出**：
```
上聯：一算二推，通三模四態五層網，構建六向七維空間，八方九域，十全智能
下聯：萬象千姿，繪九圖八景七彩畫，生成六藝五花內容，四海三江，二元生成

分析:
{'word_count': 29, 'unique_chars': 35, 'repeated_chars': '生, 成, ...', 'upper': '...', 'lower': '...'}
```

---

## 啟用虛擬環境（進階）

如果您想要直接在虛擬環境中工作：

### macOS / Linux

```bash
# 啟用虛擬環境
poetry shell

# 現在可以直接執行 Python 腳本
python demo1/demo5-1.py
python demo1/demo5-1_gemini.py
python demo1/demo5-2.py
python demo1/demo5-2_gemini.py
# ... 以此類推

# 離開虛擬環境
exit
```

### Windows

```powershell
# 啟用虛擬環境
poetry shell

# 現在可以直接執行 Python 腳本
python demo1/demo5-1.py
python demo1/demo5-1_gemini.py
python demo1/demo5-2.py
python demo1/demo5-2_gemini.py
# ... 以此類推

# 離開虛擬環境
exit
```

---

## 🎓 Runnable 物件與 LCEL 核心概念

### Runnable 物件是什麼？

Runnable 是 LangChain 的核心抽象介面，所有可執行的組件都實作了 Runnable 介面。包括：
- LLM 模型
- Prompt 模板
- Output Parser
- 自訂函數

### LCEL 表達式的優勢

**LCEL（LangChain Expression Language）** 提供了更簡潔、更直觀的方式來建立工作流程：

```python
# 傳統方式
workflow = RunnableSequence(prompt, llm, parser)

# LCEL 表達式（推薦）
workflow = prompt | llm | parser
```

### Runnable 物件類型對照表

| Runnable 類型 | 用途 | 使用時機 |
|--------------|------|---------|
| `RunnableSequence` | 順序執行 | 需要按步驟處理的任務 |
| `RunnableParallel` | 並行執行 | 需要同時執行多個獨立任務 |
| `RunnableBranch` | 條件分支 | 根據條件選擇不同的處理路徑 |
| `RunnableLambda` | 自訂函數 | 需要整合自己的 Python 函數 |
| `RunnableWithFallbacks` | 容錯機制 | 需要備援方案以提升穩定性 |
| `RunnablePassthrough` | 資料傳遞 | 需要傳遞額外資料或保留原始輸入 |

---

## 故障排除

### 問題：找不到 poetry 命令

**解決方法**：
- macOS/Linux: 將 `export PATH="$HOME/.local/bin:$PATH"` 加入 `~/.bashrc` 或 `~/.zshrc`
- Windows: 確認 Poetry 的安裝路徑已加入系統 PATH

### 問題：ModuleNotFoundError

**解決方法**：
```bash
# 確認在正確的目錄（從專案根目錄）
cd python_langchain_gemini_azure/CH5/demo1

# 重新安裝依賴
poetry install
```

### 問題：API Key 錯誤

**解決方法**：
1. 確認 `.env` 檔案位於 CH5/demo1 目錄
2. 確認 API Key 沒有多餘的空格或引號
3. 確認 API Key 仍然有效且有配額
4. 對於 Azure OpenAI，確認所有必要的環境變數都已設定

### 問題：依賴版本衝突

**解決方法**：
```bash
# 清除鎖定檔案
rm poetry.lock

# 重新解析依賴
poetry install

# 重新安裝 Google Gemini 支援
poetry add "langchain-google-genai<3.0.0"
```

### 問題：demo5-6 中的容錯機制沒有觸發

**解決方法**：
這是正常的，因為程式使用 `time.time() % 2 == 0` 來模擬隨機失敗。如果想要測試容錯機制，可以修改條件：

```python
# 改為總是失敗來測試備援機制
def unstable_advanced_model(query):
    raise Exception("LLM Service unavailable")
    return advanced_chain.invoke(query)
```

---

## 相關資源

- [LangChain 官方文檔](https://python.langchain.com/)
- [LangChain Runnable 介面文檔](https://python.langchain.com/docs/expression_language/)
- [LCEL 表達式指南](https://python.langchain.com/docs/expression_language/get_started)
- [Poetry 官方文檔](https://python-poetry.org/docs/)
- [Google Gemini API 文檔](https://ai.google.dev/docs)
- [Azure OpenAI API 文檔](https://learn.microsoft.com/azure/ai-services/openai/)



---

## 📝 結語

本章節介紹的 Runnable 物件和 LCEL 表達式是 LangChain 的核心架構，掌握這些概念後，您將能夠：

✅ 建立複雜的 AI 工作流程  
✅ 提升系統的穩定性和可維護性  
✅ 靈活處理各種實際應用場景  
✅ 為更進階的 LangChain 功能（如 Agent、RAG）打下基礎



