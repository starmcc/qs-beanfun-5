# <p align="center">🎮 QsBeanfun 5 - 秋水登錄器</p>

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/starmcc/qs-beanfun-5?label=Stars&style=flat-square)](https://github.com/starmcc/qs-beanfun-5)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](https://github.com/starmcc/qs-beanfun-5/blob/master/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/starmcc/qs-beanfun-5?display_name=tag&label=Latest&color=red&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/starmcc/qs-beanfun-5/total?label=Downloads&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/starmcc/qs-beanfun-5?label=LastCommit&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/commits/master)
[![Python](https://img.shields.io/badge/Python-3.10.11-8d38dc?style=flat-square)](https://www.python.org/)

[简体中文](./README.md) | **繁體中文** | [English](./README-EN.md)

</div>

<div align="center">
<img src="./resources/images/logo.png" width="120" height="120">
</div>

> **請注意：** QsBeanfun並不是遊戲橘子數位科技開發的官方工具，如介意請勿使用！

引用LR區域模擬元件，支援64bit臺服新楓之谷遊戲運行。

---

### 🌟 主要特色

- ✅ **支援香港/臺灣遊戲橘子登錄**
- ✅ 普通登錄、雙重登錄、QR碼登錄、官網登入
- ✅ 無需安裝遊戲橘子插件
- ✅ 模擬繁體作業系統環境運行新楓之谷
- ✅ 支援【經典版】登入

---

## 📥 安裝

[**📦點擊進入發佈頁**](https://starmcc.github.io/qs-beanfun-5/)

**下載最新 `QsBeanfun.zip` 開箱即用。**

> ⚠️ **特別注意**
> 
> `Beanfun.exe` 目錄不能存在中文，否則會出現很多未知錯誤！

---

## 🚀 實現功能

|    功能    |                    描述                    |
|:--------:|:----------------------------------------:|
| **登錄方式** | 香港/臺灣橘子 • 普通登錄 • 雙重登錄 • QR碼登錄 • GamaPass |
| **官網登入** |          原生態官網登入，解決登錄出現的各種疑難雜症           |
| **環境模擬** |             模擬繁體作業系統環境運行新楓之谷             |
| **帳號管理** |             多帳號管理，優雅的多帳號切換登入             |
| **橘子中心** |        官方儲值 • 客服中心 • 會員中心 • 用戶中心         |
| **快速啟動** |              自動屏蔽遊戲啟動視窗（可選）              |
| **更新控制** |              自動阻止遊戲自動更新（可選）              |
| **解決卡頓** |           一鍵跳過NGS進程，解決NGS卡頓問題            |
| **經典版** |               支持新楓之谷經典版登入與安裝               |
| **實用工具** |               新楓之谷實用網站快捷導航               |

---

## 🔧 環境與依賴

```bash
.venv\Scripts\activate.ps1

# 確保是清華源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
pip config get global.index-url

# 安裝套件前請自行建立 Virtualenv 虛擬環境
pip install -r requirements.txt
```

---

## 📦 打包編譯

執行 `build.bat` 檔案

```bash
# 編譯qrc檔案
pyrcc5 ./resources/resources.qrc -o ./src/Resources_rc.py
# 打包
.\build.bat
```

---

## 🔒 安全

每次發佈 `Release` `Github`都會貼出壓縮包的 (`SHA256`)

請各位下載工具後校驗 `SHA256` 值是否安全

**怎麼查詢SHA256？**

```bash
Get-FileHash -Algorithm 該程式路徑
```

*以下版本需要重新下載整個程序包*

> v5.4.1之前，賬密加密使用的是windows wmic組件，如系統缺少組件將使用默認加密密令(使用默認秘鑰)！v5.4.2已進行優化!

> **v5.6.0之後，使用PySide6構建，Python版本升級到3.10.11**

---

## 💭 結語

1. 🛡️ 所有不懷好意的指責，都需要時間去驗證和打磨。
2. 🤝 能幫助他人、分享自己的技術實現方案是一件非常愉快的事情，也希望有一些朋友一起優化它，即使只是我的一廂情願~
3. ⚠️ 凡是第三方工具都是遊戲橘子官方明令禁止使用的，最好的方式就是將系統轉為繁體語言後使用網頁登錄，望客官知悉。
4. 🎮 我只是茫茫人海中一個熱愛楓谷懂點皮毛技術的玩家，希望新楓之谷會一直營運下去，長盛不衰！

---

### 📄 使用條款

- **本軟體僅供學習使用，下載後請24小時內刪除**
- **遵循MIT開源協議**
- **如遇問題或 Bug 亦或交流，請移步 Issues**

> 🌟 最後奉勸那些指鹿為馬的傢伙，請心存善念，人生才會充滿陽光。
> 
> 🍁 楓谷作伴，瀟瀟灑灑...