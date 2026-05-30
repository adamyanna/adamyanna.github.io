# macOS Configuration Guide

> 2020-08-05

A comprehensive macOS setup reference covering terminal environment, Homebrew package management, essential applications, advanced system tweaks, and common fixes. This guide documents a complete development environment bootstrap for a freshly installed Mac.

## I. Automated Component Setup

Setting up a development environment from scratch involves several foundational components. Automating these steps ensures consistency across machines.

### 1.1 Zsh

macOS adopted Zsh as the default shell starting with Catalina (10.15). Configuring Zsh properly is the first step toward a productive terminal experience.

#### 1.1.1 .zshrc

The `.zshrc` file is the entry point for all Zsh configuration -- aliases, environment variables, PATH modifications, and plugin loading all happen here. A well-crafted `.zshrc` saves hours of repeated setup.

#### 1.1.2 Oh My Zsh

Oh My Zsh is a community-driven framework for managing Zsh configuration. It bundles thousands of helper functions, plugins, and themes.

**Installation methods:**

Via curl:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Via wget:

```bash
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Manual inspection (recommended for security-conscious users):

```bash
curl -Lo install.sh https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
sh install.sh
```

After installation, themes and plugins can be configured in `.zshrc`. Popular plugins include `git` (aliases and branch display), `docker`, `kubectl`, and `z` (fast directory jumping).

#### 1.1.3 Font

A good terminal font improves readability during long coding sessions. Nerd Fonts patches popular programming fonts with additional glyphs -- powerline symbols, devicons, and file-type icons used by many terminal themes.

Recommended: [Hack Regular Nerd Font Complete](https://github.com/ryanoasis/nerd-fonts). Hack is a monospaced typeface designed specifically for source code, with clear distinctions between similar characters (0 vs O, 1 vs l vs I).

Installation steps:
1. Download the `.ttf` file from the Nerd Fonts repository
2. Double-click to open in Font Book
3. Click "Install Font"
4. Select the font in your terminal emulator's preferences

Full collection: [nerd-fonts on GitHub](https://github.com/ryanoasis/nerd-fonts)

#### 1.1.4 Color Schemes

A thoughtfully chosen color scheme reduces eye strain and improves code scanning. The [iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes) repository provides hundreds of pre-built themes.

Popular dark schemes for long sessions:
- **Solarized Dark** -- carefully calibrated contrast ratios
- **Dracula** -- vibrant syntax highlighting on a dark purple background
- **One Dark** -- Atom editor's signature theme
- **Material** -- Google's Material Design palette

Import the `.itermcolors` file through iTerm2 Preferences > Profiles > Colors > Color Presets > Import.

### 1.2 Homebrew

Homebrew is the de facto package manager for macOS, filling the gap between the App Store and manual compilation. It installs packages to `/usr/local` (Intel) or `/opt/homebrew` (Apple Silicon).

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

After installation, verify with:

```bash
brew doctor
```

Common post-install commands:

```bash
brew update          # Update Homebrew and formula index
brew upgrade         # Upgrade all installed packages
brew search <name>   # Search for a package
brew info <name>     # Show package details
brew cleanup         # Remove old versions
```

Essential brew packages for a development workstation:

```bash
brew install git wget curl tree htop
brew install python node ruby
brew install --cask iterm2 visual-studio-code docker
```

## II. Application Manifest

A curated catalog of macOS applications organized by purpose. Each category represents a functional domain within a development workflow.

### 2.1 Development

Core development tools and IDEs:

| Category | Applications |
|---|---|
| IDEs | CLion, GoLand, PhpStorm, PyCharm, Visual Studio Code |
| Database | Navicat Premium, Postman |
| Documentation | Dash (offline API docs), MacDown (Markdown editor), Typora |
| Containers | Docker |
| Diagramming | OmniGraffle, MindNode, XMind ZEN |
| Terminal | iTerm2 |
| Editors | Sublime Text |
| Diff/Merge | Beyond Compare |
| Office | Microsoft Office |

JetBrains IDEs (CLion, GoLand, PhpStorm, PyCharm) provide deep language-specific intelligence. Visual Studio Code serves as the lightweight, polyglot editor for quick edits and web projects. Dash provides instant offline access to 200+ API documentation sets with fuzzy search.

Postman streamlines API development with request collections, environment variables, and automated testing scripts. Beyond Compare handles complex diff and merge operations beyond what git provides by default.

### 2.2 Networking

Network connectivity and proxy tools:

- **OneDrive** -- cloud file synchronization
- **Proxifier** -- force applications through SOCKS/HTTP proxies
- **ShadowsocksX-NG-R8** -- secure proxy client

Proxifier is particularly useful when certain development tools do not natively support proxy configurations. It transparently redirects application traffic at the system level.

### 2.3 Tools

System utilities and productivity enhancers:

| Tool | Purpose |
|---|---|
| Alfred 3 | Spotlight replacement with workflows |
| Android File Transfer | Android device file browser |
| Blackmagic Disk Speed Test | Storage benchmarking |
| CleanMyMac X | System cleanup and optimization |
| DaisyDisk | Disk space visualization |
| Firefox | Secondary browser for web development |
| gfxCardStatus | GPU switching monitor for dual-GPU MacBooks |
| Google Chrome | Primary browser and DevTools |
| HandShaker | Android device management |
| iHosts | Hosts file manager with group switching |
| IINA | Modern media player (mpv-based) |
| iStat Menus | Menu bar system monitors (CPU, memory, network, disk, temps) |
| Karabiner-Elements | Keyboard customizer and remapper |
| Karabiner-EventViewer | Keyboard event debugger |
| Kindle | E-book reader |
| Magnet | Window snapping and management |
| NightOwl | Toggle light/dark mode per-app |
| Parallels Desktop | Virtualization for Windows/Linux |
| Speedtest | Network bandwidth testing |
| TG Pro | Fan control and temperature monitoring |
| Typeeto | Use Mac keyboard as Bluetooth keyboard for other devices |
| VLC | Universal media player |

Karabiner-Elements deserves special mention: it allows complex key remappings, including per-application rules. For developers switching between macOS and external keyboards, or users of custom mechanical keyboards, it provides fine-grained control over every key.

### 2.4 Open Source

- **AirBar** -- open-source menu bar utility

### 2.5 Chinese Market Applications

Applications commonly used within the Chinese ecosystem:

- **QQ** -- instant messaging
- **WeChat** -- messaging and social platform
- **WeChat Work** -- enterprise communication

### 2.6 Trial Software Download Sites

Resources for discovering and evaluating macOS software:

- [nmac.to](https://nmac.to)
- [xclient.info](https://xclient.info)

## III. Advanced Configuration

System-level tweaks that go beyond the default macOS experience.

### 3.1 Disable Gatekeeper

Gatekeeper blocks applications from unidentified developers. Disabling it allows running unsigned software (common with open-source tools and development builds):

```bash
sudo spctl --master-disable
```

Re-enable with:

```bash
sudo spctl --master-enable
```

Use this cautiously. Only disable Gatekeeper if you understand the security implications and trust the sources of your software.

### 3.2 Add Spacer Tiles to Dock

Create visual separators in the Dock for grouping related applications:

```bash
defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="spacer-tile";}'
killall Dock
```

Run this command multiple times to add several spacers. Drag them within the Dock to position them between app clusters (e.g., separating development tools from communication apps).

### 3.3 CLI Sublime Text Launcher

Enable launching Sublime Text from the terminal with the `subl` command:

```bash
sudo ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl
```

Verify the symlink is on your PATH:

```bash
cd /usr/local/bin
echo $PATH
```

Usage examples:

```bash
subl .                    # Open current directory in Sublime Text
subl file.txt             # Open a single file
subl -n project/          # Open in a new window
```

### 3.4 RIME Input Method: Squirrel

[RIME (Squirrel)](https://rime.im/) is a highly customizable Chinese input method engine for macOS. Unlike commercial input methods, RIME is open-source, offline-first, and respects user privacy. It supports multiple Chinese input schemas including Pinyin, Wubi, Cangjie, and Zhuyin.

Key advantages:
- No network dependency -- works entirely offline
- No telemetry or data collection
- Configurable via YAML files for custom dictionaries and shortcuts
- Supports traditional and simplified Chinese

Configuration files reside in `~/Library/Rime/`. Custom dictionaries and input schemas can be added to tailor the experience to specific vocabulary domains (technical, legal, medical).

## IV. Troubleshooting

Common macOS issues and their fixes.

### 4.1 Fix No Audio Output

When audio suddenly stops working (typically after sleep/wake cycles or Bluetooth device disconnections), restart the CoreAudio daemon:

```bash
sudo launchctl stop com.apple.audio.coreaudiod && sudo launchctl start com.apple.audio.coreaudiod
```

This restarts the audio subsystem without requiring a full reboot. The `&&` ensures the daemon is stopped before attempting to restart it.

### 4.2 Flush DNS Cache

DNS issues manifest as some websites loading while others do not, or stale DNS records after changing nameservers. Flush the cache with:

```bash
sudo killall -HUP mDNSResponder
sudo killall mDNSResponderHelper
sudo dscacheutil -flushcache
```

The `-HUP` signal (hangup) instructs mDNSResponder to reload its configuration rather than terminate. The DNS cache utility purge removes locally cached DNS entries. Together, these force all subsequent name resolutions to query upstream DNS servers fresh.

### 4.3 Bluetooth Channel Optimization and Connection Repair

Bluetooth interference causes audio dropouts, laggy peripherals, and random disconnections -- especially problematic in dense office environments with many competing 2.4 GHz devices.

**Procedure:**

1. Download **Additional Tools for Xcode** from [Apple Developer Downloads](https://developer.apple.com/download/more/?=for%20Xcode). This is a separate bundle from Xcode itself, containing debugging and diagnostic utilities.

2. Open the `Additional_Tools_for_Xcode.dmg` disk image.

3. Navigate to the `Hardware` directory and locate **Bluetooth Explorer**.

4. Launch Bluetooth Explorer. From the menu bar, select **Tools > RSSI Sweeper**.

5. Click **Start**. The Bluetooth module will temporarily disconnect as it scans the surrounding radio environment. It analyzes which channels other Bluetooth connections are using and selects the optimal channel with the least interference for your active connections.

This is a one-time optimization that persists until the RF environment changes significantly (e.g., you move to a different room, new devices appear). Run it whenever Bluetooth performance degrades.

**How it works:** Bluetooth operates across 40 channels in the 2.4 GHz ISM band (2402-2480 MHz). The RSSI Sweeper measures received signal strength on each channel, identifying which are congested. The Bluetooth controller then adjusts its adaptive frequency hopping map to prefer cleaner channels, improving both throughput and connection stability.

---

**Related resources:**
- [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)
- [iTerm2 Color Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes)
- [Homebrew](https://brew.sh/)
- [RIME Input Method](https://rime.im/)
