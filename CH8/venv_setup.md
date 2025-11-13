# Python venv 環境設定指南

本指南說明如何從 Poetry 改用 Python venv 來管理專案依賴。

## 前置需求

- Python 3.11 或以上版本
- pip（通常隨 Python 一起安裝）

## 步驟 1：建立虛擬環境

在專案目錄（CH8）中執行以下命令：

```bash
cd CH8
```

```bash
python -m venv venv
```



這會在當前目錄建立一個名為 `venv` 的虛擬環境資料夾。

## 步驟 2：啟動虛擬環境

### macOS/Linux:

```bash
source venv/bin/activate
```

### Windows:


#### 使用 PowerShell（如果遇到執行原則錯誤）

如果 PowerShell 顯示類似以下的錯誤：
```
無法載入檔案，因為這個系統上已停用指令碼執行
```

**解決方案 A：修改執行原則（推薦）**

在 PowerShell 中執行（以系統管理員身分執行）：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

然後再執行：

```powershell
venv\Scripts\Activate.ps1
```

或

```powershell
.\venv\Scripts\Activate.ps1
```

**解決方案 B：暫時繞過執行原則（僅本次工作階段）**

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
venv\Scripts\Activate.ps1
```

**解決方案 C：使用 CMD 啟動虛擬環境**

如果不想修改執行原則，可以在 PowerShell 中執行：

```powershell
cmd /k venv\Scripts\activate.bat
```

**解決方案 D：使用完整路徑**

```powershell
& .\venv\Scripts\Activate.ps1
```

啟動成功後，命令列提示字元前面會顯示 `(venv)`。

## 步驟 3：升級 pip（建議）

```bash
pip install --upgrade pip
```

## 步驟 4：安裝專案依賴套件

 `requirements.txt` 檔案，可以使用：

```bash
pip install -r requirements.txt
```

## 步驟 5：驗證安裝

確認所有套件都已正確安裝：

```bash
pip list
```

## 建立 requirements.txt（選用）

如果您想要建立 `requirements.txt` 檔案以便日後使用，可以在虛擬環境中執行：

```bash
pip freeze > requirements.txt
```

## 注意事項

1. **虛擬環境資料夾**：`venv` 資料夾應該加入 `.gitignore`，不要提交到版本控制系統。

2. **每次使用前**：記得先啟動虛擬環境（步驟 2），才能使用已安裝的套件。

3. **Python 版本**：確保使用 Python 3.11 或以上版本。

4. **依賴版本**：上述安裝命令使用 `>=` 來指定最低版本要求，這與 Poetry 的 `^` 語義類似。

5. **PowerShell 執行原則**：
   - 如果遇到「無法載入檔案，因為這個系統上已停用指令碼執行」的錯誤，請參考步驟 2 中的解決方案。
   - 推薦使用 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`，這只會影響當前使用者，且安全性較高。
   - 如果不想修改執行原則，可以使用 CMD 或透過 `cmd /k` 在 PowerShell 中執行。

## 快速參考

### macOS/Linux:

```bash
# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 安裝套件
pip install -r requirements.txt

# 停用虛擬環境
deactivate
```

### Windows (PowerShell):

```powershell
# 建立虛擬環境
python -m venv venv

# 修改執行原則（僅需執行一次）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 安裝套件
pip install -r requirements.txt

# 停用虛擬環境
deactivate
```

### Windows (CMD):

```cmd
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
venv\Scripts\activate

# 安裝套件
pip install -r requirements.txt

# 停用虛擬環境
deactivate
```

