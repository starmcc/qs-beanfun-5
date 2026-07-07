# <p align="center">QsBeanfun 5 - 秋水登录器</p>

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/starmcc/qs-beanfun-5?label=Stars&style=flat-square)](https://github.com/starmcc/qs-beanfun-5)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](https://github.com/starmcc/qs-beanfun-5/blob/master/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/starmcc/qs-beanfun-5?display_name=tag&label=Latest&color=red&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/starmcc/qs-beanfun-5/total?label=Downloads&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/starmcc/qs-beanfun-5?label=LastCommit&style=flat-square)](https://github.com/starmcc/qs-beanfun-5/commits/master)
[![Python](https://img.shields.io/badge/Python-3.10.11-8d38dc?style=flat-square)](https://www.python.org/)

**简体中文** | [繁體中文](./README-TW.md)

</div>

<div align="center">
<img src="./resources/images/logo.png" width="120" height="120">
</div>

> **请注意：** QsBeanfun并不是游戏橘子数位科技开发的官方工具，如介意请勿使用！

引用LR区域模拟元件，支持64bit台服新枫之谷游戏运行。

---

### 🌟 主要特性

- ✅ **支持香港/台湾游戏橘子登录**
- ✅ 普通登录、双重登录、二维码登录、官网登入
- ✅ 无需安装游戏橘子插件
- ✅ 模拟繁体操作系统环境运行新枫之谷

---

## 📥 安装

[**📦点击进入发布页**](https://starmcc.github.io/qs-beanfun-5/)

**下载最新 `QsBeanfun.zip` 开箱即用。**

> ⚠️ **特别注意**
> 
> `Beanfun.exe` 目录不能存在中文，否则会出现很多未知错误！

---

## 🚀 实现功能

|    功能    |              描述               |
|:--------:|:-----------------------------:|
| **登录方式** | 香港/台湾橘子 • 普通登录 • 双重登录 • 二维码登录 |
| **官网登入** |     原生态官网登入，解决登录出现的各种疑难杂症     |
| **环境模拟** |       模拟繁体操作系统环境运行新枫之谷        |
| **账号管理** |       多账号管理，优雅的多账号切换登入        |
| **橘子中心** |   官方储值 • 客服中心 • 会员中心 • 用户中心   |
| **快速启动** |        自动屏蔽游戏启动窗口（可选）         |
| **更新控制** |        自动阻止游戏自动更新（可选）         |
| **解决卡顿** |      一键跳过NGS进程，解决NGS卡顿问题      |
| **实用工具** |         新枫之谷实用网站快捷导航          |

---

## 🔧 环境与依赖

```bash
# 确保是清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
pip config get global.index-url

# 安装包前请自行创建 Virtualenv 虚拟环境
pip install -r requirements.txt
```

---

## 📦 打包编译

执行 `build.bat` 文件

```bash
# 编译qrc文件
pyrcc6 ./resources/resources.qrc -o ./src/Resources_rc.py
# 打包
.\build.bat
```

---

## 🔒 安全

每次发布 `Release` `Github`都会贴出压缩包的 (`SHA256`)

请各位下载工具后校验 `SHA256` 值是否安全

**怎么查询SHA256？**

```bash
Get-FileHash -Algorithm 该程序路径
```

*以下版本需要重新下载整个程序包*

> v5.4.1之前，账密加密使用的是windows wmic组件，如系统缺少组件将使用默认加密密令，将使用默认秘钥！v5.4.2已进行优化!

> v5.6.0之后，使用PySide6构建，Python版本升级到3.10.11

---

## 💭 结语

1. 🛡️ 所有不怀好意的指责，都需要时间去验证和打磨。
2. 🤝 能帮助他人、分享自己的技术实现方案是一件非常愉快的事情，也希望有一些朋友一起优化它，即使只是我的一厢情愿~
3. ⚠️ 凡是第三方工具都是游戏橘子官方明令禁止使用的，最好的方式就是将系统转为繁体语言后使用网页登录，望客官知悉。
4. 🎮 我只是茫茫人海中一个热爱枫谷懂点皮毛技术的玩家，希望新枫之谷会一直运营下去，长盛不衰！

---

### 📄 使用条款

- **本软件仅供学习使用，下载后请24小时内删除**
- **遵循MIT开源协议**
- **如遇问题或 Bug 亦或交流，请移步 Issues**

> 🌟 最后奉劝那些指鹿为马的家伙，请心存善念，人生才会充满阳光。
> 
> 🍁 枫谷作伴，潇潇洒洒...

---

# 赞赏

如果您也觉得本项目对您有所帮助，请慷慨的为作者送上一笔赞赏。

在此的每一笔犒劳都将让作者铭记于心！

<image style="width: 200px; height: 200px;" src="./Appreciate.png"></image>

> 打赏大佬名单，由近到远依次排列~

名单中是微信名，如果想用游戏名请在备注上填写哦~

再次感谢各位大佬的赞赏，天使定会亲吻善良的你~

如不想展示可单独联系我删除名字，部分并未展示是实在找不到您的名字

> 名单更新时间：2025-9-27

|                   赞赏名单 | 款项（RMB） |
|-----------------------:|:--------|
|                     杀手 | 50      |
|                    无名氏 | 520     |
|                    无名氏 | 200     |
|                    李素雅 | 20.24   |
|                   泡泡茶壶 | 1       |
|                   基泥胎美 | 20      |
|                  华(中国) | 20      |
|                    奎秃子 | 10      |
|                Andr*** | 20      |
|        COSMOS(PS:喝杯奶茶) | 30      |
|                    咳咳溜 | 20      |
|                  不再犹豫z | 66      |
|                   索德渃斯 | 50      |
|                     九号 | 10      |
|                   Mr·铭 | 20      |
|          A酷田照明-专业美缝-小陈 | 10      |
|                  tiger | 100     |
|          阿樑（PS：谢谢作者大大） | 10      |
|                    稻草人 | 50      |
|                    JS. | 30      |
|                     Li | 18.88   |
|                    无所谓 | 20      |
|                    潘治文 | 5       |
|                 J-hard | 10      |
|                    李素雅 | 10      |
|                     莫心 | 10      |
|                      1 | 10      |
|            我。（PS：感谢感谢） | 20      |
|                 俾面嗌声林生 | 10      |
|         今天雨下好大（PS：辛苦了） | 10      |
|              不爱喝阿萨姆的萨满 | 10      |
|                    发条橙 | 10      |
|                     晨辉 | 20      |
|                徐小姐的黑脸将 | 10      |
|                 COOKIE | 50      |
|                    吹吹风 | 38      |
| like sunshine（PS:中杯奶茶） | 22      |
|                    周小明 | 20      |
|             阿里跨境^O^陈明初 | 110     |
|                  Lydia | 10      |
|                   百年孤寂 | 10      |
|                    Azu | 10      |
|                     Kk | 5       |
|                   鸣Zai | 10      |
|                  心（符号） | 20      |
