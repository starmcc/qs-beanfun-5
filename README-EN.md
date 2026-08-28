# <p align="center">🎮 QsBeanfun 5 - QiuShui Login Tool</p>

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/starmcc/qs-beanfun-5?label=Stars&style=flat-square)](https://github.com/starmcc/qs-beanfun-5)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](https://github.com/starmcc/qs-beanfun-5/blob/master/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/starmcc/qs-beanfun-5?display_name=tag&label=Latest&color=red&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/starmcc/qs-beanfun-5/total?label=Downloads&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/starmcc/qs-beanfun-5?label=LastCommit&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/commits/master)
[![Python](https://img.shields.io/badge/Python-3.10.11-8d38dc?style=flat-square)](https://www.python.org/)

[简体中文](./README.md) | [繁體中文](./README-TW.md) | **English**

</div>

<div align="center">
<img src="./resources/images/logo.png" width="120" height="120">
</div>

> **Please note:** QsBeanfun is **not** an official tool developed by Gamania Digital Entertainment. If you are not comfortable with this, please do not use it!

Uses the LR region emulation component to support running the 64-bit Taiwan MapleStory client.

---

### 🌟 Key Features

- ✅ **Supports Hong Kong / Taiwan Gamania login**
- ✅ Standard login, two-factor login, QR code login, official website login
- ✅ No need to install the Gamania plugin
- ✅ Emulates a Traditional Chinese OS environment to run MapleStory
- ✅ Supports 【Classic】login

---

## 📥 Installation

[**📦 Click to visit the release page**](https://starmcc.github.io/qs-beanfun-5/)

**Download the latest `QsBeanfun.zip` and use it out of the box.**

> ⚠️ **Important**
>
> The `Beanfun.exe` directory must not contain Chinese characters, otherwise many unknown errors may occur!

---

## 🚀 Implemented Features

|    Feature    |                    Description                    |
|:------------:|:------------------------------------------------:|
| **Login Methods** | Hong Kong/Taiwan Gamania • Standard login • Two-factor login • QR code login • GamaPass |
| **Official Login** | Native official website login, resolving various login issues |
| **Environment Emulation** | Emulates a Traditional Chinese OS environment to run MapleStory |
| **Account Management** | Multi-account management with elegant account switching |
| **Gamania Center** | Official recharge • Customer service • Member center • User center |
| **Quick Launch** | Automatically dismisses the game launch window (optional) |
| **Update Control** | Automatically blocks game auto-updates (optional) |
| **Fix Lag** | One-click skip of the NGS process to resolve NGS lag issues |
| **Classic** | Supports MapleStory Classic login and installation |
| **Utilities** | Quick navigation to useful MapleStory websites |

---

## 🔧 Environment & Dependencies

```bash
.venv\Scripts\activate.ps1

# Make sure to use the Tsinghua mirror
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
pip config get global.index-url

# Create a Virtualenv virtual environment before installing packages
pip install -r requirements.txt
```

---

## 📦 Build & Package

Run the `build.bat` file

```bash
# Compile the qrc file
pyrcc5 ./resources/resources.qrc -o ./src/Resources_rc.py
# Package
.\build.bat
```

---

## 🔒 Security

Every `Release` on `GitHub` includes the compressed package's (`SHA256`)

Please verify the `SHA256` value after downloading the tool to ensure it is safe

**How to check SHA256?**

```bash
Get-FileHash -Algorithm <path to the program>
```

*The following versions require re-downloading the entire package*

> Before v5.4.1, account/password encryption used the Windows wmic component. If the system lacks the component, the default encryption key is used! This was optimized in v5.4.2!

> **After v5.6.0, built with PySide6, Python version upgraded to 3.10.11**

---

## 💭 Closing Thoughts

1. 🛡️ All malicious accusations need time to be verified and refined.
2. 🤝 Helping others and sharing technical solutions is a very enjoyable thing. I also hope some friends will help optimize it, even if it's just my wishful thinking~
3. ⚠️ All third-party tools are explicitly prohibited by Gamania Digital Entertainment. The best approach is to switch the system to Traditional Chinese and use web login. Please be aware.
4. 🎮 I am just a player who loves MapleStory and knows a little bit of technology among the vast crowd. I hope MapleStory will keep running and prosper forever!

---

### 📄 Terms of Use

- **This software is for learning purposes only. Please delete it within 24 hours after downloading**
- **Follows the MIT open-source license**
- **If you encounter issues, bugs, or want to discuss, please visit Issues**

> 🌟 Finally, to those who call a deer a horse, please be kind, and your life will be full of sunshine.
>
> 🍁 With MapleStory as company, carefree and free-spirited...
