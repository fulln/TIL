## git 版本的回滚

有时候git提交错误需要回滚，这里总结下回滚相关的命令

- 查看git 提交日志
`git log`

### 只修改本地的git

- 查看git 本地的操作日志

          git reflog

- 修改最近一次提交的comments

          git commit --amend

- 撤销最近一次的提交，并保留提交内容

          git reset HEAD^

### 修改已经提交的git

- 修改某一次提交的内容（很大概率导致冲突）

先用日志看你想修改的commitid，然后使用

     git rebase -i "your commit id" 
     
这个时候会进入一个文件中，然后提示在你需要修改的分支之后有多行commit要修改，如果你要修改哪一行commit，就把那行的pick改成edit，然后保存退出，这个时候你再查看git log，最后一次提交已经变成了你的选择的那行commit，这个时候再去修改你需要修改的内容，
然后使用

     git rebase --continue
     
保存修改的内容，再用

     git push -f  origin master
     
将修改提到远程

- 直接回滚到某一次提交之前（最省事

这样会导致所有commit之后的内容，日志都会丢失，谨慎使用.

    git reset --hard your commit id 

这个是本地分支的，使用

    git push -f origin master
    
强制提交，这样远程的分支也会回滚到你指定的提交前

 
