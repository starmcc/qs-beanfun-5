
<p align="center">
    <a target="_blank" href="https://github.com/dream-core/qs-beanfun-5">
        <img alt="stars" src="https://img.shields.io/github/stars/dream-core/qs-beanfun-5?label=Stars"/>
    </a>    
    <a target="_blank" href="https://github.com/dream-core/qs-beanfun-5/blob/master/LICENSE">
        <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-lightgrey"/>
    </a>
    <a target="_blank" href="https://github.com/dream-core/qs-beanfun-5/releases/latest">
        <img alt="Releases" src="https://img.shields.io/github/v/release/dream-core/qs-beanfun-5?display_name=tag&label=Latest&color=red"/>
    </a>
  </p>
<p align="center">
    <a target="_blank" href="https://github.com/dream-core/qs-beanfun-5/releases/latest">
        <img alt="Downloads" src="https://img.shields.io/github/downloads/dream-core/qs-beanfun-5/total?label=Downloads"/>
    </a>
    <a target="_blank" href="https://github.com/dream-core/qs-beanfun-5/commits/master">
        <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/dream-core/qs-beanfun-5?label=LastCommit">
    </a>
    <a target="_blank" href="https://www.python.org/">
        <img alt="JRE" src="https://img.shields.io/badge/Python-3.9.6-8d38dc"/>
    </a>
</p>
<p align="center">
    <span style="font-weight:bold;">简体中文</span>
    <a href="./README-TW.md">繁體中文</a>
</p>


## 介紹

Please forgive me for not writing this document in English.

I don't have a lot of energy to do it.

秋水登錄器並不是遊戲橘子數位科技開發的官方工具

引用LR區域模擬元件，支持32/64bit臺服新楓之谷遊戲運行。

> 支持香港/臺灣遊戲橘子登錄

**遵循MIT開源協議**，如遇問題或 Bug 亦或交流，請移步 Issues。

## 安裝

[**Releases-點擊進入下載頁面**](https://github.com/dream-core/qs-beanfun-5/releases)

**下載最新`Beanfun.zip`開箱即用。**

> **特別註意**

`Beanfun.exe`目錄不能存在中文，否則無法啟動遊戲

## 實現功能

| 功能                                              |
|-------------------------------------------------|
| 香港/臺灣橘子 <br/>普通登錄、雙重登錄、二維碼登錄<br/>Ps: 無需安裝遊戲橘子插件 |
| 模擬繁體操作系統環境運行[新楓之谷]                              |
| 用戶中心 -> 充值、客服、會員中心、賬號詳情                         |
| 免輸賬密啟動/進入遊戲                                     |
| 自動屏蔽遊戲啟動窗口（可選）                                  |
| 自動阻止遊戲自動更新（可選）                                  | 
| 一鍵跳過NGS進程                                       | 
| 新楓之谷實用網站快捷導航                                    |

## 環境與依賴

```
# 確保是清華源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
pip config get global.index-url

# 安裝包前請自行創建 Virtualenv 虛擬環境
pip install -r requirements.txt
```

# 打包編譯

執行`build.bat`文件

```
.\build.bat
```

## 安全

每次發布`Release`都會貼出壓縮包的(`Hash`)哈希值

請各位下載工具後校驗`Hash`值是否安全

怎麼查詢哈希值？

```
certutil -hashfile 該程序路徑
```

回車後會出現hash值。

## 結語

1. 所有不懷好意的指責，都需要時間去驗證和打磨。
2. 能幫助他人、分享自己的技術實現方案是一件非常愉快的事情，也希望有一些朋友一起優化它，即使只是我的一廂情願~~
3. 凡是第三方工具都是遊戲橘子官方明令禁止使用的，最好的方式就是將系統轉為繁體語言後使用網頁登錄，望客官知悉。
4. 我只是茫茫人海中一個熱愛楓谷懂點皮毛技術的玩家，希望新楓之谷會一直運營下去，長盛不衰！

**<p style="font-size:18px">本軟件僅供學習使用，下載後請24小時內刪除</p>**
**<p style="font-size:22px">遵循MIT開源協議</p>**

最後奉勸那些指鹿為馬的家夥，請心存善念，人生才會充滿陽光。

> 楓谷作伴，瀟瀟灑灑...