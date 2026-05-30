# macOS Setup 2025

> 2025

A fresh macOS development environment setup — terminal, input methods, Homebrew, and essential tooling for polyglot engineering workflows.

## Input Methods

Multi-language keyboard input configuration for English, French, and Chinese:

| Layout | Input Method | Use Case |
|---|---|---|
| **US English** | Built-in | Primary development keyboard |
| **CA Français** | Built-in | Canadian French documents and correspondence |
| **CN Pinyin** | [Rime (rime-ice)](https://github.com/iDvel/rime-ice) | Chinese character input with ICE phonetics |

### Why Rime?

Rime is an open-source, cross-platform input method engine. The `rime-ice` configuration provides:

- Pinyin input with fuzzy matching
- Emoji and symbol dictionary
- English word completion within Chinese input
- Customizable schemas via YAML

Install via Homebrew:

```bash
brew install --cask squirrel
```

Then place the `rime-ice` configuration in `~/Library/Rime/`.

## Terminal & Shell

### iTerm2

```bash
brew install --cask iterm2
```

Recommended profile settings:
- **Font**: JetBrains Mono 13pt with ligatures enabled
- **Theme**: Solarized Dark (custom)
- **Transparency**: 8% background blur

### Oh My Zsh

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Essential plugins:

```bash
plugins=(git docker kubectl zsh-autosuggestions zsh-syntax-highlighting fzf)
```

## Homebrew & CLI Tooling

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Core packages

```bash
brew install \
  git gh \
  python@3.13 go node \
  kubernetes-cli helm kubectx \
  jq yq wget htop \
  neovim tmux \
  ripgrep fd bat eza \
  openssl readline sqlite3
```

### Development fonts

```bash
brew install --cask font-jetbrains-mono font-fira-code font-hack-nerd-font
```

## macOS System Preferences

```bash
# Show hidden files in Finder
defaults write com.apple.finder AppleShowAllFiles -bool true

# Show path bar
defaults write com.apple.finder ShowPathbar -bool true

# Disable press-and-hold for keys (faster key repeat for coding)
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false

# Fast key repeat rate
defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15

# Save screenshots to Downloads
defaults write com.apple.screencapture location ~/Downloads

killall Finder
```

## Essential Applications

| App | Purpose | Install |
|---|---|---|
| **VS Code** | Primary editor | `brew install --cask visual-studio-code` |
| **Docker Desktop** | Container runtime | `brew install --cask docker` |
| **Obsidian** | Notes & knowledge base | `brew install --cask obsidian` |
| **Rectangle** | Window management | `brew install --cask rectangle` |
| **AltTab** | Windows-style alt-tab | `brew install --cask alt-tab` |
| **Keka** | Archive extraction | `brew install --cask keka` |

## Git Configuration

```bash
git config --global user.name "Adam"
git config --global user.email "adam@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global core.editor "nvim"
git config --global alias.lg "log --oneline --graph --all"
```

## References

- [Homebrew](https://brew.sh/)
- [Oh My Zsh](https://ohmyz.sh/)
- [Rime ICE](https://github.com/iDvel/rime-ice)
- [macOS Setup Guide (thoughtbot)](https://github.com/thoughtbot/laptop)
