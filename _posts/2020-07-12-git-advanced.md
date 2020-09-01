---
title: Git进阶
author: Teddy
date: 2020-07-12 12:30:48 +0800
categories: [实践, 开发工具]
tags: [Git]
---

# Git 进阶用法

## I. Git CLI 高级用法

### 1. 重置头部指针

```shell
git reset {commitHash}/HEAD~{number} --hard
```

* 可以使用此命令重置当前提交的指针，将指针放在一个特定的提交上，如果想要远端达到相同的效果则需要 `--force` 强制推送远端，此命令生效后，会导致重置的哈稀值之前的提交都不在提交记录中
* `--hard`表示强制重置

```shell
git reflog
```

* 使用`reflog`命令可以再次看到`reset`之前的提交的哈稀值，再次使用`git reset`可以重新回到之前的提交点

### 2. 合并多次已同步远端的提交

```shell
git rebase -i {commitHash}/HEAD~{number}
```

* 使用`rebase -i`指定到你想要合并的提交的**前一个**提交的哈稀值上，完成后会进入`vim`模式

```shell
pick 2f2fcb4d2 "{commit message}"
pick 3f4a9e8e6 "{commit message}"
pick 5f4a7e8e6 "{commit message}"
```

* 提交顺序为倒序，*最下面的是最新的提交*，此处有两种方式可以合并下面两个提交到第一行的最老的提交上
  * 使用关键词 `squash` 或者 `s` （`s`是缩写形式）替换掉第二行和第三行的 `pick`，完成之后`ESC: w`保存修改，然后退出，此时在查看 `git log` 可以发现出现了一个新的提交，并且描述信息和第一行的相同，而且**原本的三个提交记录仍然存在**
  
  * 使用关键词 `fixup` 替换掉第二行和第三行的 `pick`，完成之后`ESC: w`保存修改，然后退出，此时在查看 `git log` 可以发现出现了一个新的提交，并且描述信息和第一行的相同，而且**原本的三个提交记录已经不存在了**
  
    >pick：保留该commit（缩写:p）
    >reword：保留该commit，但我需要修改该commit的注释（缩写:r）
    >edit：保留该commit, 但我要停下来修改该提交(不仅仅修改注释)（缩写:e）
    >squash：将该commit和前一个commit合并（缩写:s）
    >fixup：将该commit和前一个commit合并，但我不要保留该提交的注释信息（缩写:f）
    >exec：执行shell命令（缩写:x）
    >drop：我要丢弃该commit（缩写:d）

```shell
git push -f origin {branch_name}:{branch_name}
```

* 强制推到远端仓库，与远端仓库同步此次修改

### 3. 清除工作区域和暂存区所有修改和文件

```shell
git clean -df
```

### 4. 只将同一文件中的部分修改移动到暂存区

```shell
git add --patch 
```

* 使用 `git add --patch`  （或者简称 `-p`），`git` 会开始把你的文件分解成它认为合理的"大块"(文件的一部分)。然后，它将提示以下问题：

```shell
Stage this hunk [y,n,q,a,d,/,g,s,e,?]?
```

* 以下是每个选项的说明：

> `Y` 为下一次提交准备这个模块
> `n`不为下一次提交准备此块
> `q` 退出；不要将此块或任何剩余块放入阶段
> `a` 将此块和文件中的所有后续块放入阶段
> `d` 不准备此块或文件中的任何后期块
> `g` 选择要转到的块
> `/` 搜索与给定regex匹配的块
> `s` 将当前的大块拆分为较小的大块
> `e` 手动编辑当前hunk
> `?` 打印Hunk帮助

* 如果文件还不在存储库中，可以先执行 `git add -N` 。然后你可以继续使用 `git add -p` 

```shell
git diff --staged
```

* 检查是否进行了正确的更改

```shell
git reset -p
```

* `reset` 到 `unstage` 错误地添加了大块

```shell
git commit -v
```

* 在编辑提交消息时查看提交
* 注 `git format-patch` ，该命令的目的是将提交数据解析为.patch文件。

### 5. 撤销一次非merge的Commit

```shell
git revert {commitHash}
```

### 6. 强制拉取当前HEAD的新增修改

```shell
git pull --rebase
```

* 对于，使用 `git add --amend` 和 `git push -f` 强制提交到同一commit的提交，如果需要在另一个本地仓库拉取同步使用 `git pull` 会要求解决冲突并重新提交，使用 `git pull --rebase` 可以直接强制拉取并重新将`HEAD` 指向远端最新修改；

### 7. 文件从暂存区回退到工作区

```shell
git reset HEAD {file_name}
```

### 8. 单独挑选任意一个提交到当前分支

```shell
git cherry-pick {commitHash}
```

* 有冲突的情况下，需要单独处理冲突

### 9. 将多个提交并入当前分支

```shell
git rebase   [startpoint]   [endpoint]  --onto  [branchName]
git checkout [branchName]
git reset --hard [endpoint]
```

* (startpoint, endpoint] 从开始 `commitHash` 到结束 `commitHash` 是一个前开后闭的区间，需要考虑当前要并入那些提交
* 完成 `rebase` 后，需要reset当前分支的 `HEAD` 指针

### 10. 将当前开发分支的Base同步为最新的master或CI

```shell
git rebase master
```

* 将当前分支的Base分支更新为最新的master



## II. Git 思维方法论 - 底层代码分析