---
name: commit
description: Create a new commit for all of our uncommitted changes
---

Create a new commit for all of our uncommitted changes
run git status && git diff HEAD && git status --porcelain to see what files are uncommitted
add the untracked and changed files
if you see any files that should not be committed such as build artifacts, add them to .gitignore and do not include them in the commit

Add an atomic commit message with an appropriate message

add a tag such as "feat", "fix", "docs", etc. that reflects our work
