```
─(utyfull㉿kali)-[~]

└─$ cd Desktop

┌──(utyfull㉿kali)-[~/Desktop]

└─$ ls

git

┌──(utyfull㉿kali)-[~/Desktop]

└─$ cd git

┌──(utyfull㉿kali)-[~/Desktop/git]

└─$ mkdir Labs\_inf

┌──(utyfull㉿kali)-[~/Desktop/git]

└─$ cd Labs\_inf

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf]

└─$ git init

Initialized empty Git repository in /home/utyfull/Desktop/git/Labs\_inf/.git/

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf]

└─$ git status

On branch master

No commits yet

nothing to commit (create/copy files and use "git add" to track)

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf]

└─$ git clone https://github.com/utyfull/labs\_inf.git

Cloning into 'labs\_inf'...

remote: Enumerating objects: 13, done.

remote: Counting objects: 100% (13/13), done.

remote: Compressing objects: 100% (8/8), done.

remote: Total 13 (delta 1), reused 5 (delta 0), pack-reused 0

Receiving objects: 100% (13/13), done.

Resolving deltas: 100% (1/1), done.

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf]

└─$ git status

On branch master

No commits yet

Untracked files:

(use "git add <file>..." to include in what will be committed)

labs\_inf/

nothing added to commit but untracked files present (use "git add" to track)

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf]

└─$ ls

labs\_inf

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf]

└─$ cd labs\_inf

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ ls

README.md

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status
On branch main

Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ nano Hello.txt

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch main

Your branch is up to date with 'origin/main'.

Untracked files:

(use "git add <file>..." to include in what will be committed)

Hello.txt

nothing added to commit but untracked files present (use "git add" to track)

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git add .

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch main

Your branch is up to date with 'origin/main'.

Changes to be committed:

(use "git restore --staged <file>..." to unstage)

new file:

Hello.txt

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git commit

[main 5436aa4] Hello file

1 file changed, 1 insertion(+)

create mode 100644 Hello.txt

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch main

Your branch is ahead of 'origin/main' by 1 commit.

(use "git push" to publish your local commits)

nothing to commit, working tree clean

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git push

giUsername for 'https://github.com': utyfull

Password for 'https://giutyfull@github.com':

Enumerating objects: 4, done.

Counting objects: 100% (4/4), done.

Delta compression using up to 4 threads

Compressing objects: 100% (2/2), done.

Writing objects: 100% (3/3), 279 bytes | 279.00 KiB/s, done.

Total 3 (delta 0), reused 0 (delta 0), pack-reused 0

To https://github.com/utyfull/labs\_inf.git

fa01324..5436aa4 main -> main

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch main

Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git revert HEAD

[main 9deed6d] Revert "Hello file"

1 file changed, 1 deletion(-)

delete mode 100644 Hello.txt

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch main

Your branch is ahead of 'origin/main' by 1 commit.

(use "git push" to publish your local commits)

nothing to commit, working tree clean

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git push

Enumerating objects: 3, done.

Counting objects: 100% (3/3), done.

Delta compression using up to 4 threads

Compressing objects: 100% (1/1), done.

Writing objects: 100% (2/2), 259 bytes | 259.00 KiB/s, done.

Total 2 (delta 0), reused 1 (delta 0), pack-reused 0

To https://github.com/utyfull/labs\_inf.git

5436aa4..9deed6d main -> main

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ ls

1

README.md

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ mkdir 1

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ touch 1/ .placeholder

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch main

Your branch is up to date with 'origin/main'.

Untracked files:

(use "git add <file>..." to include in what will be committed)

.placeholder

nothing added to commit but untracked files present (use "git add" to track)

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git add .

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git commit -m "Empty directory for lab"

[main 71e761d] Empty directory for lab

1 file changed, 0 insertions(+), 0 deletions(-)

create mode 100644 .placeholder

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git push

Enumerating objects: 4, done.

Counting objects: 100% (4/4), done.

Delta compression using up to 4 threads

Compressing objects: 100% (2/2), done.

Writing objects: 100% (3/3), 287 bytes | 287.00 KiB/s, done.

Total 3 (delta 0), reused 1 (delta 0), pack-reused 0

To https://github.com/utyfull/labs\_inf.git

9deed6d..71e761d main -> main

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git checkout -b test\_branch

Switched to a new branch 'test\_branch'

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch test\_branch

nothing to commit, working tree clean

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git push origin test\_branch

git status

Total 0 (delta 0), reused 0 (delta 0), pack-reused 0

remote:

remote: Create a pull request for 'test\_branch' on GitHub by visiting:

remote:

remote:

https://github.com/utyfull/labs\_inf/pull/new/test\_branch

To https://github.com/utyfull/labs\_inf.git

\* [new branch] test\_branch -> test\_branch

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ git status

On branch test\_branch

nothing to commit, working tree clean

┌──(utyfull㉿kali)-[~/Desktop/git/Labs\_inf/labs\_inf]

└─$ cd 1

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ ls

Markdown\_console\_listening.md

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git status

On branch test\_branch

Untracked files:

(use "git add <file>..." to include in what will be committed)

./

nothing added to commit but untracked files present (use "git add" to track)

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git add .

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git status

On branch test\_branch

Changes to be committed:

(use "git restore --staged <file>..." to unstage)

new file:

Markdown\_console\_listening.md

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git commit -m "Markdown listening"

[test\_branch 66af10d] Markdown listening

1 file changed, 0 insertions(+), 0 deletions(-)

create mode 100644 1/Markdown\_console\_listening.md

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git push origin test\_branch

Enumerating objects: 5, done.

Counting objects: 100% (5/5), done.

Delta compression using up to 4 threads

Compressing objects: 100% (4/4), done.

Writing objects: 100% (4/4), 7.38 KiB | 7.38 MiB/s, done.

Total 4 (delta 0), reused 0 (delta 0), pack-reused 0

To https://github.com/utyfull/labs\_inf.git

71e761d..66af10d test\_branch -> test\_branch

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ nano otchet.txt

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git status

On branch test\_branch

Untracked files:

(use "git add <file>..." to include in what will be committed)

otchet.txt

nothing added to commit but untracked files present (use "git add" to track)

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git add .

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git commit -m "Otchet"

[test\_branch 52b9bcb] Otchet

1 file changed, 4 insertions(+)

create mode 100644 1/otchet.txt

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git push

fatal: The current branch test\_branch has no upstream branch.

To push the current branch and set the remote as upstream, use

git push --set-upstream origin test\_branch

To have this happen automatically for branches without a tracking

upstream, see 'push.autoSetupRemote' in 'git help config'.

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git push origin test\_branch

Enumerating objects: 6, done.

Counting objects: 100% (6/6), done.

Delta compression using up to 4 threads

Compressing objects: 100% (4/4), done.

Writing objects: 100% (4/4), 909 bytes | 909.00 KiB/s, done.

Total 4 (delta 0), reused 0 (delta 0), pack-reused 0

To https://github.com/utyfull/labs\_inf.git

66af10d..52b9bcb test\_branch -> test\_branch

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git status

On branch test\_branch

Changes not staged for commit:

(use "git add <file>..." to update what will be committed)

(use "git restore <file>..." to discard changes in working directory)

modified:

Markdown\_console\_listening.md

no changes added to commit (use "git add" and/or "git commit -a")

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git add .

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git commit -m "Modif md"

[test\_branch 7199cac] Modif md

1 file changed, 0 insertions(+), 0 deletions(-)

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git push origin test\_branch

Enumerating objects: 7, done.

Counting objects: 100% (7/7), done.

Delta compression using up to 4 threads

Compressing objects: 100% (4/4), done.

Writing objects: 100% (4/4), 1.64 KiB | 1.64 MiB/s, done.

Total 4 (delta 0), reused 0 (delta 0), pack-reused 0

To https://github.com/utyfull/labs\_inf.git

52b9bcb..7199cac test\_branch -> test\_branch

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git checkout main

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git merge test\_branch

Already up to date.

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git switch main

Switched to branch 'main'

Your branch is up to date with 'origin/main'.

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git push origin -d test\_branch

To https://github.com/utyfull/labs\_inf.git

\- [deleted]

test\_branch

┌──(utyfull㉿kali)-[~/…/git/Labs\_inf/labs\_inf/1]

└─$ git status

On branch main

Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

