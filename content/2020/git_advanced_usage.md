# Git Advanced Usage

> 2020-07-12

Advanced Git CLI techniques — reset strategies, interactive rebase, partial staging, cherry-picking, and force-pull workflows for day-to-day engineering.

## 1. Reset HEAD Pointer

```bash
git reset {commitHash}/HEAD~{number} --hard

```

Moves the current branch pointer to a specific commit. To replicate on the remote, force-push (`--force`). All commits after the target hash are removed from the log.

**Recovery:** `git reflog` shows all recent HEAD movements, including those "lost" by reset. You can `git reset` back to any reflog entry.

## 2. Squash Multiple Commits (Already Pushed)

```bash
git rebase -i {commitHash}/HEAD~{number}

```

Specify the commit hash **before** the first one you want to squash. Enters vim with:

```

pick 2f2fcb4d2 "commit message"
pick 3f4a9e8e6 "commit message"
pick 5f4a7e8e6 "commit message"

```

Commits are listed in reverse chronological order (newest at bottom).

### Rebase Keywords

| Keyword | Abbrev | Effect |
|---|---|---|
| `pick` | p | Keep this commit |
| `reword` | r | Keep but edit the commit message |
| `edit` | e | Keep but pause to amend (code + message) |
| `squash` | s | Merge into previous commit, keep both messages |
| `fixup` | f | Merge into previous commit, discard this message |
| `exec` | x | Run a shell command |
| `drop` | d | Remove this commit |

**Key difference:** `squash` keeps the original commit records visible in reflog; `fixup` discards them.

```bash
git push -f origin {branch}:{branch}

```

Force-push to sync the rewritten history with the remote.

## 3. Clean Working Directory

```bash
git clean -df

```

Removes all untracked files and directories (`-d` = directories, `-f` = force).

## 4. Stage Partial File Changes (Patch Mode)

```bash
git add --patch       # or -p

```

Git decomposes the file into "hunks" and prompts for each:

| Option | Action |
|---|---|
| `y` | Stage this hunk |
| `n` | Skip this hunk |
| `q` | Quit; stage nothing further |
| `a` | Stage this hunk and all remaining hunks in the file |
| `d` | Skip this hunk and all remaining hunks |
| `g` | Jump to a specific hunk |
| `/` | Search for a hunk matching regex |
| `s` | Split current hunk into smaller hunks |
| `e` | Manually edit the current hunk |
| `?` | Print help |

**New file workflow:**

```bash
git add -N {file}      # Intent-to-add (track an untracked file)
git add -p             # Stage selectively
git diff --staged      # Verify staged changes
git reset -p           # Unstage incorrectly staged hunks
git commit -v          # Commit with diff visible in editor

```

## 5. Revert a Non-Merge Commit

```bash
git revert {commitHash}

```

Creates a new commit that undoes the specified commit's changes. Safe for shared branches — does not rewrite history.

## 6. Force-Pull (Rebase Local onto Remote)

```bash
git pull --rebase

```

When a remote branch has been force-pushed (e.g., after `git add --amend` + `git push -f`), a regular `git pull` would require conflict resolution. `git pull --rebase` directly rebases your local HEAD onto the remote tip.

## 7. Unstage Files (Stage → Working)

```bash
git reset HEAD {file_name}

```

## 8. Cherry-Pick a Single Commit

```bash
git cherry-pick {commitHash}

```

Applies a specific commit onto the current branch. Resolve conflicts manually if they arise.

## 9. Rebase a Range of Commits

```bash
git rebase [startpoint] [endpoint]

```

Applies a commit range onto the current branch, preserving linear history.

## 10. Generate Patch Files

```bash
git format-patch

```

Serializes commits into `.patch` files for email-based workflows or offline review.
