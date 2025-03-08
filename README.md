### **README.md**

# 🏗️ Python 虛擬環境設定與迷宮腳本使用指南

本專案包含用於**生成**、**編輯**和**解決**迷宮的 Python 腳本。為了確保順利運行，提供了一系列自動化腳本來**建立**、**啟動**和**管理** Python 虛擬環境。

## 📦 需求的 Python 套件
此專案需要以下 Python 套件：
- `numpy`
- `matplotlib`
- `tkinter`（Python 內建，但某些系統可能需要手動安裝）

☝️ 目前只有在 `python 3.12` 上測試過，但其實更早更早的版本應該也可以

---

## 📜 腳本說明

### 🛠️ `setup_env.bat` / `setup_env.ps1`
- 建立 Python 虛擬環境 (`venv/`)。
- 安裝所需的 Python 套件 (`numpy`、`matplotlib`、`tkinter`)。
- 確保環境可用於執行迷宮腳本。

### 🚀 `activate_env.bat` / `activate_env.ps1`
- 啟動虛擬環境。
- 開啟命令提示字元，讓使用者可以手動執行腳本。

### 🏗️ `pattern_gen.py`
- 生成隨機的 17x17 迷宮。
- 根據特定規則放置 **劍（2）** 和 **怪物（3）**。
- 將生成的迷宮存成 `.txt` 文件。

#### 命令行參數說明
```bash
python pattern_gen.py [--num-patterns N] [--write-mode MODE] [--no-swords-no-monsters 0|1] [--only-swords 0|1] [--swords-and-monsters 0|1] [--detour-swords 0|1]
```

- `--num-patterns N`: 生成迷宮的數量（預設: 10）
- `--write-mode MODE`: 文件寫入模式，'a'為追加，'w'為覆寫（預設: 'a'）
- `--no-swords-no-monsters 0|1`: 是否生成無劍無怪物的迷宮（預設: 1 = 是）
- `--only-swords 0|1`: 是否生成只有劍的迷宮（預設: 1 = 是）
- `--swords-and-monsters 0|1`: 是否生成有劍和怪物的迷宮（預設: 1 = 是）
- `--detour-swords 0|1`: 是否生成需要繞路取劍的迷宮（預設: 1 = 是）

**範例：**
```bash
# 生成5個迷宮，所有類型都包含
python pattern_gen.py --num-patterns 5

# 生成10個迷宮，覆寫現有檔案而非追加
python pattern_gen.py --write-mode w

# 只生成有劍和怪物的迷宮，不生成其他類型
python pattern_gen.py --no-swords-no-monsters 0 --only-swords 0 --detour-swords 0 --swords-and-monsters 1
```

### 🖍️ `pattern_edit.py`
- 提供 **圖形化介面（GUI）** 來編輯迷宮。
- 允許使用者修改牆壁、道路、劍、怪物的位置。
  - 對各方格左/右鍵點擊，即可循序更換方格
- 確保迷宮符合特定條件
  - 是否有唯一路線，且可以通過
  - 是否僅在偶數行列放置牆壁

### 📈 ~~`pattern_viz.py`~~
- ~~沒用到~~

---

## 📄 資料說明

### 根據 `pattern_gen.py` 生成的迷宮，有三種可能的樣式：
#### `swords_and_monsters.txt`
- 在唯一路線上，依序會遇到劍與怪物
#### `no_swords_no_monsters.txt`
- 在唯一路線上，沒有劍與怪物
#### `only_swords.txt`
- 在唯一路線上，只有劍，沒有怪物
#### `detour_swords.txt`
- 在唯一路線上，有怪物，但是劍在偏離路線且可以到達的地方
#### ~~`input.txt`~~
- ~~沒用到~~

### `<目前使用中 pattern 檔案>_edited.txt`
- 使用 `pattern_edit.py` 編輯迷宮完，按下 `Save Pattern` 按鈕，會將編輯後的迷宮寫在此檔案

---

## 🖥️ 安裝與使用方式

### 🔹 **Windows（批次腳本 .bat）**
#### 0️⃣ **下載下來**
廢話...
```bat
git clone https://github.com/weintried/lab02-pattern-tools.git
```
你要用 zip 下載下來也不是不行啦

#### 1️⃣ **建立虛擬環境**
執行 `setup_env.bat`：
```bat
setup_env.bat
```
此腳本將會：
- 創建一個虛擬環境 (`venv/`)。
- 安裝必要的 Python 套件。

🉑 此腳本只需要在第一次使用時執行

#### 2️⃣ **啟動虛擬環境**
執行 `activate_env.bat`：
```bat
activate_env.bat
```
此腳本將會：
- 啟動虛擬環境。
- 開啟命令提示字元，讓你可以執行 Python 腳本。

🉑 每次要使用時，都使用這個腳本開啟命令行

#### 3️⃣ **執行迷宮腳本**
啟動環境後，會跳出命令行，可以執行：
```bat
python pattern_gen.py
python pattern_edit.py <欲使用之 pattern 檔案>.txt
```

---

### 🔹 **Windows（PowerShell 腳本 .ps1）**
如果你更喜歡使用 **PowerShell**，請執行以下指令：

#### 1️⃣ **建立虛擬環境**
```powershell
.\setup_env.ps1
```

#### 2️⃣ **啟動虛擬環境**
```powershell
.\activate_env.ps1
```

#### 3️⃣ **執行迷宮腳本**
```powershell
python pattern_gen.py
python pattern_edit.py maze_patterns.txt
```

⚠ **PowerShell 執行安全性提醒**：  
如果遇到安全性錯誤，請執行：
```powershell
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```
這將允許執行自訂 PowerShell 腳本。

---

### 🔹 **Linux/macOS（手動安裝）**
對於 **Linux/macOS** 用戶，可以手動建立與啟動虛擬環境：

#### 1️⃣ **建立虛擬環境**
```sh
python3 -m venv venv
```

#### 2️⃣ **啟動虛擬環境**
```sh
source venv/bin/activate
```

#### 3️⃣ **安裝必要的 Python 套件**
```sh
pip install numpy matplotlib tk
```

#### 4️⃣ **執行迷宮腳本**
```sh
python pattern_gen.py
python pattern_edit.py maze_patterns.txt
```

---

## 🚮 如何刪除

將整個 `venv` 賽料夾刪除，即可刪除環境

將整個 clone 下來的資料夾刪除，即可刪除全部資料

---

## ❓ 常見問題與疑難排解

- **找不到虛擬環境？**
  - 請先執行 `setup_env.bat` 建立環境。

- **PowerShell 無法執行 `.ps1` 腳本？**
  - 請開啟 PowerShell 並執行：
    ```powershell
    Set-ExecutionPolicy Unrestricted -Scope CurrentUser
    ```

- **在 Linux/macOS 上 `tkinter` 無法使用？**
  - 你可能需要手動安裝 `tkinter`：
    ```sh
    sudo apt-get install python3-tk
    ```

---

## 📝 授權條款
本專案為 **AI 生成**，我真的要被取代了，耶！🚀

