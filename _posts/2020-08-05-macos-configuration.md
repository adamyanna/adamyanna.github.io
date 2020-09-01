---
title: MacOS配置
author: Teddy
date: 2020-08-05 08:40:51 +0800
categories: [规划, 工作流]
tags: [MacOS]
---

# MacOS 配置

## I. 自动化组件部署

### 1.1 ZSH

#### 1.1.1 zshrc

[.zshrc]({{ "/assets/files/zsh" | relative_url }})

#### 1.1.2 Oh My Zsh

##### download

* [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)

##### via curl

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

##### via wget

```shell
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

##### Manual inspection

```shell
curl -Lo install.sh https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
sh install.sh
```

#### 1.1.3 Font

* [nerd-fonts](https://github.com/ryanoasis/nerd-fonts)

* [Hack Regular Nerd Font Complete](https://github.com/ryanoasis/nerd-fonts/blob/master/patched-fonts/Hack/Regular/complete/Hack%20Regular%20Nerd%20Font%20Complete.ttf)

#### 1.1.4 Color

* [iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes)

### 1.2 Brew

##### download

* [Homebrew](https://brew.sh/)

##### install

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```



## II. 应用程序

### 2.1 开发

* Beyond Compare
* CLion
* Dash
* Docker
* GoLand
* iTerm
* MacDown
* MindNode
* Office
* Navicat Premium
* OmniGraffle
* PhpStorm
* Postman
* PyCharm
* Sublime Text
* Typora
* Visual Studio Code
* XMind ZEN

### 2.2 网络

* OneDrive
* Proxifier
* ShadowsocksX-NG-R8

### 2.3 工具

* Blackmagic Disk Speed Test
* Alfred 3
* Android File Transfer
* CleanMyMac X
* DaisyDisk
* Firefox
* gfxCardStatus - video card switcher
* Google Chrome
* HandShaker
* iHosts
* IINA
* iStat Menus
* Karabiner-Elements
* Karabiner-EventViewer
* Kindle
* Magnet
* NightOwl
* Parallels Desktop
* Speedtest
* TG Pro
* Typeeto
* VLC

### 2.4 开源

* AirBar

### 2.5 墙内

* QQ
* WeChat
* WeChat Work

### 2.6 试用软件下载站点

* [nmac.to](nmac.to)
* [xclient.info](xclient.info)



## III. 高级配置

### 3.1 关闭"不明身份开发者"检查

```shell
sudo spctl --master-disable
```

### 3.2 Dock中增加空格图标做分隔符

```shell
defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="spacer-tile";}'
killall Dock
```

### 3.3 CLI启动sublime
```shell
sudo ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl
cd /usr/local/bin
echo $PATH
```

### 3.4 高效的中文输入法

* 【鼠鬚管】輸入法

## IV. 问题修复

### 4.1 修复MacOS音频无声音的问题

```shell
sudo launchctl stop com.apple.audio.coreaudiod && sudo launchctl start com.apple.audio.coreaudiod
```

### 4.2 清除当前dns缓存

```shell
sudo killall -HUP mDNSResponder
sudo killall mDNSResponderHelper
sudo dscacheutil -flushcache
```

### 4.3 蓝牙信道优化、连接修复
* 下载 Additional_Tools_for_Xcode [Tools_for_Xcode](https://developer.apple.com/download/more/?=for%20Xcode)
* 打开 `Additional_Tools_for_Xcode.dmg` 选择 `Hardware` > `Bluetooth Explorer` ，进入 `Bluetooth Explorer` 的 `menu bar` 选择 `Tools > RSSI Sweeper`
* `start` 后蓝牙会暂时端口，蓝牙模块在扫描到其他蓝牙连接的信道后，会优化当前连接的信道，保证最优质的连接


