# f-surfing client

本项目代码源于以下项目：

GDCTSCP：https://github.com/GDCTSCP/GDCTSCP  
由于对 GDCTSCP 项目进行了重写，修改了部分逻辑，对 Windows 做了些兼容处理，同时增强了代码的可读性，因此脱离 GDCTSCP 成立一个新的分支。

本项目是佛大广东天翼校园客户端在 Linux 下的解决方案，如果需要佛大 iNode 客户端在 Linux 下的解决方案，请移步：https://github.com/KiritoA/c3h_client


## 概述

 - 本项目是基于 GDCTSCP 进行修改的，感谢 @mynuolr 先前作出的努力与贡献
 - 测试环境为佛大
 - Python 版本为 2.7
 - 在 OpenWrt CHAOS CALMER (15.05, r46767) （ramips mt7620）下测试通过
 - 可跨平台运行于 Windows/Linux/OpenWrt(基于 Linux 的智能路由器操作系统)
 - 在本项目的研究过程中，本人依然遵守校方的“一人一号”规则（即本人所在宿舍是每人一个宽带账号的），本项目的研究目的是为了本人的设备在 Linux 平台（官方未提供 Linux 平台的软件）下能够正常接入校园网
 
## 使用方法

### 配置

首先修改 `fsurfing.py` 中的账号密码：
```python
# 学号
USERNAME = "StudentID"

# 天翼客户端的密码，非 iNode 的密码
PASSWORD = "Password"
```
另外，还有一个可选配置，如果是佛大的学生则无需修改，其他学校需要自行抓包查看：
```python
NASIP = "113.105.243.254"
```

### 运行
在 Linux 环境中，直接运行 `./fsurfing.py` 即可。

在 OpenWrt 环境下，如果没有安装 Python，可按照以下命令安装：  
（如果你需要路由器，可以在网上购买一些“硬改”过的二手路由器，搜索关键词为 “二手路由器 硬改 OpenWrt”，推荐 `TP-LINK TL-WR740N`，售价大约是 35 元。） 

Barrier Breaker 14.07：
```bash
opkg update
opkg install python-mini
```
Chaos Calmer 15.05：
```bash
opkg update
# 如果你的闪存只有 8MB，建议安装 python-base，大约 1MB
opkg install python-base
# 如果你的闪存大于 16MB，可以安装 python-light，大约 7.5MB
opkg install python-light
```
如果你安装的是 `mini` 版或者是 `light` 版，可能会缺少一些库，可以使用 `check-dependence.py` 来进行检测，然后把缺少的库手动复制上去。


## 开源协议

本项目遵循 GNU GPLv3 开源协议，这意味着：  
你可以免费使用、引用和修改本项目的代码以及衍生代码，但不允许将修改后和衍生的代码做为闭源的**商业**软件发布和销售。