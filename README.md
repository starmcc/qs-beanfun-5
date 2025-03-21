# QsBeanfun 5 - 秋水登录器

<p align="center">
    <a target="_blank" href="https://github.com/starmcc/qs-beanfun">
        <img alt="stars" src="https://img.shields.io/github/stars/starmcc/qs-beanfun?label=Stars"/>
    </a>    
    <a target="_blank" href="https://github.com/starmcc/qs-beanfun/blob/master/LICENSE">
        <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-lightgrey"/>
    </a>
    <a target="_blank" href="https://github.com/starmcc/qs-beanfun/releases/latest">
        <img alt="Releases" src="https://img.shields.io/github/v/release/starmcc/qs-beanfun?display_name=tag&label=Latest&color=red"/>
    </a>
  </p>
<p align="center">
    <a target="_blank" href="https://github.com/starmcc/qs-beanfun/releases/latest">
        <img alt="Downloads" src="https://img.shields.io/github/downloads/starmcc/qs-beanfun/total?label=Downloads"/>
    </a>
    <a target="_blank" href="https://github.com/starmcc/qs-beanfun/commits/master">
        <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/starmcc/qs-beanfun?label=LastCommit">
    </a>
    <a target="_blank" href="https://www.oracle.com/java/technologies/downloads/#jre8-windows">
        <img alt="JRE" src="https://img.shields.io/badge/Python-3.9.6-8d38dc"/>
    </a>
</p>
<p align="center">
    <span style="font-weight:bold;">简体中文</span>
    <a href="./README-TW.md">繁體中文</a>
</p>

## 介绍

Please forgive me for not writing this document in English.

I don't have a lot of energy to do it.

秋水登录器并不是游戏橘子数位科技开发的官方工具

引用LR区域模拟元件，支持32/64bit台服新枫之谷游戏运行。

> 支持登录方式

1. 香港账号 - (账密/双重验证)
2. 台湾账号 - (账密/二维码/QR码)
3. 内置各种实用小功能

**遵循MIT开源协议**，如遇问题或 Bug 亦或交流，请移步 Issues。

## 安装

[**Releases-点击进入下载页面**](https://github.com/starmcc/qs-beanfun/releases)

**下载最新`QsBeanfun.zip`开箱即用。**

> **特别注意**

`QsBeanfun.exe`目录不能存在中文，否则无法启动游戏

## 实现功能

| 功能                                              |
|-------------------------------------------------|
| 香港/台湾橘子 <br/>普通登录、双重登录、二维码登录<br/>Ps: 無需安裝游戏橘子插件 |
| 模拟繁体操作系统环境运行[新楓之谷]                              |
| 用户中心 -> 充值、客服、会员中心、账户详情                         |
| 免输账密启动/进入游戏                                     |
| 自动屏蔽游戏启动窗口（可选）                                  |
| 自动阻止游戏自动更新（可选）                                  | 
| 一键跳过NGS进程                                       | 
| 新枫之谷实用网站快捷导航                                    |

## 环境与依赖

```
# 确保是清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
pip config get global.index-url

# 安装包前请自行创建 Virtualenv 虚拟环境
pip install -r requirements.txt
# 编译QRC资源文件 请在pipenv环境中执行
pyrcc5.exe .\src\Resources.qrc -o .\src\Resources_rc.py
```

# 打包编译

执行`build.bat`文件

```
.\build.bat
```

## 安全

每次发布`Release`都会贴出压缩包的(`Hash`)哈希值

请各位下载工具后校验`Hash`值是否安全

怎麽查询哈希值？

```
certutil -hashfile 该程序路径
```

回车后会出现hash值。

## 结语

1. 所有不怀好意的指责，都需要时间去验证和打磨。
2. 能帮助他人、分享自己的技术实现方案是一件非常愉快的事情，也希望有一些朋友一起优化它，即使只是我的一厢情愿~~
3. 凡是第三方工具都是游戏橘子官方明令禁止使用的，最好的方式就是将系统转为繁体语言后使用网页登录，望客官知悉。
4. 我只是茫茫人海中一个热爱枫谷懂点皮毛技术的玩家，希望新枫之谷会一直运营下去，长盛不衰！

**<p style="font-size:18px">本软件仅供学习使用，下载后请24小时内删除</p>**
**<p style="font-size:22px">遵循MIT开源协议</p>**

最后奉劝那些指鹿为马的家伙，请心存善念，人生才会充满阳光。

> 枫谷作伴，潇潇洒洒...

# 赞赏

如果您也觉得本项目对您有所帮助，请慷慨的为作者送上一笔赞赏。

在此的每一笔犒劳都将让作者铭记于心！

<image style="width: 200px; height: 200px;" src="./Appreciate.png"></image>

> 打赏大佬名单，由近到远依次排列~

名单中是微信名，如果想用游戏名请在备注上填写哦~

再次感谢各位大佬的赞赏，天使定会亲吻善良的你~

如不想展示可单独联系我删除名字，部分并未展示是实在找不到您的名字

> 名单更新时间：2024-7-29

|           名单           | 金额（RMB） |
|:----------------------:|:-------:|
|          无名氏           |   200   |
|          李素雅           |  20.24  |
|          泡泡茶壶          |    1    |
|          基泥胎美          |   20    |
|         华(中国)          |   20    |
|          奎秃子           |   10    |
|        Andr***         |   20    |
|    COSMOS(PS:喝杯奶茶)     |   30    |
|          咳咳溜           |   20    |
|         不再犹豫z          |   66    |
|          索德渃斯          |   50    |
|           九号           |   10    |
|          Mr·铭          |   20    |
|     A酷田照明-专业美缝-小陈      |   10    |
|         tiger          |   100   |
|     阿樑（PS：谢谢作者大大）      |   10    |
|          稻草人           |   50    |
|          JS.           |   30    |
|           Li           |  18.88  |
|          无所谓           |   20    |
|          潘治文           |    5    |
|         J-hard         |   10    |
|          李素雅           |   10    |
|           莫心           |   10    |
|           1            |   10    |
|      我。（PS：感谢感谢）       |   20    |
|         俾面嗌声林生         |   10    |
|     今天雨下好大（PS：辛苦了）     |   10    |
|       不爱喝阿萨姆的萨满        |   10    |
|          发条橙           |   10    |
|           晨辉           |   20    |
|        徐小姐的黑脸将         |   10    |
|         COOKIE         |   50    |
|          吹吹风           |   38    |
| like sunshine（PS:中杯奶茶） |   22    |
|          周小明           |   20    |
|       阿里跨境^O^陈明初       |   110   |
|         Lydia          |   10    |
|          百年孤寂          |   10    |
|          Azu           |   10    |
|           Kk           |    5    |
|          鸣Zai          |   10    |
|         心（符号）          |   20    |

