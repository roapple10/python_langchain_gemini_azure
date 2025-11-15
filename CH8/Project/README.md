# 🎬 Gemini 影片與圖片分析工具

一個基於 Google Gemini AI 和 Streamlit 的互動式多模態分析應用程式，可以分析影片內容、識別圖片，並回答關於影片和圖片的問題。

## ✨ 功能特色

- 📹 **影片內容分析**：上傳影片檔案，AI 自動分析影片內容
- 🖼️ **圖片比對分析**：可選上傳圖片，與影片內容進行比對
- 💬 **智能問答**：使用自然語言提問，獲得詳細的分析結果
- 🎯 **多種分析模式**：
  - 影片內容摘要
  - 對話內容提取
  - 人物識別與時間定位
- 📊 **即時進度顯示**：顯示檔案上傳、處理和分析的即時進度
- 🚀 **簡單易用**：直觀的 Web 介面，無需編程知識

## 🛠️ 技術棧

- **前端框架**：Streamlit
- **AI 模型**：Google Gemini (gemini-1.5-flash-latest)
- **Python 版本**：3.11+
- **主要套件**：
  - `streamlit` - Web 應用框架
  - `google-generativeai` - Google Gemini API
  - `python-dotenv` - 環境變數管理

## 📋 環境需求

- Python 3.11 或更高版本
- Google Gemini API Key（免費申請：[Google AI Studio](https://ai.google.dev)）
- 穩定的網路連線（用於上傳檔案和 API 呼叫）

## 🚀 安裝步驟

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

或使用 Poetry（如果專案使用 Poetry 管理）：

```bash
poetry install
```

### 2. 設定環境變數

在專案根目錄（`CH8` 資料夾）建立 `.env` 檔案：

```env
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL_ID=gemini-1.5-flash-latest
```

**取得 API Key：**
1. 前往 [Google AI Studio](https://ai.google.dev)
2. 點擊「Get API key」
3. 建立新的 API Key 或選擇現有專案
4. 複製 API Key 並貼到 `.env` 檔案中

> 💡 **提示**：Google AI Studio 提供免費額度，無需綁定信用卡！

## 🎮 使用說明

### 啟動應用程式

在 `Project` 資料夾內執行：

在 `ch8` 資料夾內執行：

#### 使用 pip 安裝方式

```bash
streamlit run Project/streamlit_app.py
```

#### 使用 Poetry 管理環境

```bash
poetry run streamlit run Project/streamlit_app.py
```

應用程式會自動在瀏覽器中開啟（通常是 `http://localhost:8501`）
...existing code...
應用程式會自動在瀏覽器中開啟（通常是 `http://localhost:8501`）

### 操作步驟

1. **上傳影片檔案**
   - 點擊「選擇影片檔案」
   - 支援格式：MP4、MOV、AVI、MKV
   - 檔案大小建議：不超過 100MB（視 API 限制而定）

2. **上傳圖片檔案**（可選）
   - 點擊「選擇圖片檔案」
   - 支援格式：JPG、JPEG、PNG、GIF、WEBP
   - 用於與影片內容進行比對分析

3. **輸入問題**
   - 在文字框中輸入您想問的問題
   - 或點擊快速問題範例按鈕：
     - **範例 1**：影片內容摘要
     - **範例 2**：列出所有對話
     - **範例 3**：比對圖片人物

4. **開始分析**
   - 點擊「🚀 開始分析」按鈕
   - 等待處理完成（會顯示進度條）
   - 查看分析結果

### 問題範例

- 「請問你從影片中看到什麼？用繁體中文回答。」
- 「請詳細地條列出影片中每個人所說的話，用繁體中文回答。」
- 「請問影片中有沒有出現圖片裡的這個人，在第幾秒，他說了什麼，用繁體中文回答。」

## 📝 功能說明

### 影片分析流程

1. **檔案上傳**：將影片上傳到 Google AI 伺服器
2. **處理等待**：等待 Google AI 處理影片（可能需要數分鐘）
3. **AI 分析**：使用 Gemini 模型分析影片內容
4. **結果顯示**：在介面上顯示分析結果

### 多模態分析

當同時上傳影片和圖片時，AI 可以：
- 識別影片中是否出現圖片中的人物
- 定位人物出現的時間點
- 提取該時間點的對話內容
- 進行視覺比對分析

## ⚠️ 注意事項

- **處理時間**：影片上傳和處理需要時間，大型檔案可能需要數分鐘
- **檔案大小限制**：請注意 Google API 的檔案大小限制
- **API 額度**：免費 API 有每分鐘請求數限制（15 RPM）
- **網路連線**：需要穩定的網路連線進行檔案上傳
- **臨時檔案**：應用程式會自動清理臨時檔案

## 🔧 疑難排解

### 問題：無法啟動應用程式

**解決方案**：
- 確認已安裝所有依賴：`pip install -r requirements.txt`
- 確認 Python 版本為 3.11 或更高

### 問題：API Key 錯誤

**解決方案**：
- 確認 `.env` 檔案位於 `CH8` 資料夾（不是 `Project` 資料夾）
- 確認 API Key 格式正確，沒有多餘的空格
- 確認 API Key 在 Google AI Studio 中有效

### 問題：影片處理失敗

**解決方案**：
- 確認影片格式支援（MP4、MOV、AVI、MKV）
- 確認檔案大小未超過限制
- 檢查網路連線是否穩定
- 稍後再試（可能是 API 暫時性問題）

### 問題：處理時間過長

**解決方案**：
- 這是正常現象，影片處理需要時間
- 大型檔案可能需要 5-10 分鐘
- 請耐心等待，不要關閉瀏覽器視窗

## 📚 相關資源

- [Google AI Studio](https://ai.google.dev) - 申請 API Key
- [Streamlit 文件](https://docs.streamlit.io/) - Streamlit 使用指南
- [Gemini API 文件](https://ai.google.dev/docs) - Gemini API 參考文件

## 📄 授權

本專案僅供學習使用。

---

**Powered by Google Gemini AI | Streamlit**
