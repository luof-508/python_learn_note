# git：  

多人并行协作开发。同时修改一个函数，修改不一样，合并的时候遇到冲突怎办。不同人提交的修改就是分支，多个分支最后合并，通过版本管理，否则并行开发乱套了。

## 1. 概念
[git概念示意图](git概念示意图.PNG)  
**repository，版本库**：分为远程仓库和本地仓库，要管理的文件都放到仓库里。`git init`初始化后，会在当前目录生成一个`.git`目录，这个目录就是版本库

**工作区，workspace**：`.git`所在的目录就是工作区，一般时项目的根目录。注意：工作区不是指`.git`目录，是指`.git`位于的那个目录，比如`.git`位于notes目录，则notes目录内都是工作区，`.git`被隐藏，也不要再`.git`目录内工作，因为搞不好就破坏了版本库，无法和远端库通信。

**index，索引、暂存区**：介于工作区和版本库之间，暂时缓存修改的，通过`git add filename`，将修改的文件放入index。

**commit，确认**：`git commit`，将暂存区的目录加入版本库，

**remote，远端版本库**：便于多人项目开发，在github等服务器上创建的版本库，可以和本地库交互。通过`git push`，将本地库修改push到远端库，`git pull`拉取远端库从而将修改更新到本地库。

**push**：工作区workspace(代码的编辑环境)  -add->  索引index(待提交)  -commit->  本地仓库repository  -push->  remote。

**pull**: remote  -pull->  workspace  

## 2. git使用
### 2.1初始化一个版本库：
`git init`，执行后，就会在当前目录生产`.git`目录，即版本库。

### 2.2 添加一个`index.html`文件到暂存区：
`git add index.html`；`git add`，不接文件，将所有修改添加到暂存区，不建议这样用，除非清楚的知道自己修改了哪些文件。添加前和添加后，通过通过`git status`，查看文件状态分别为：  
**添加前**：  
>Untracked files:  
  (use "git add <file>..." to include in what will be committed)  
        index.html  

**添加后**：  
>Changes to be committed:  
  (use "git rm --cached <file>..." to unstage)  
        new file:   index.html  

也就是说，添加前，**修改过的文件**未被跟踪管理，修改未保存这样不安全，比如好不容易码了一天，不小心删除了，找不回来。添加后，就变成被跟踪管理的文件了，即使被删了，也能从暂存区恢复。 总之，通过`git add filename`，把文件**当前变化**增加到暂存区管理起来。暂存后，再次修改可再次暂存，还可以暂存新文件可以通过`git add .` 将当前目录变化的文件批量递归的添加到暂存区。
[git staged life cycle](git_staged_life_cycle.PNG)
### 2.3忽略列表`.gitignore`： 
由2，通过`git status`，可以查看当前工作区文件状态，可以看到哪些**修改过的文件**没有被跟踪管理。这里涉及到不需要跟踪的文件，即忽略ignored的文件。`.gitignore`文件就是忽略列表。这个文件不需要自己写，python已经有了。

### 2.4 提交代码`git commit`：
比如提交刚刚暂存的`index.html`文件。`git commit -m "First commit" index.html`。注意，一定要加"-m"，即message，后面写修改描述（因为什么问题，修改了哪些文件、哪些函数，等等），便于跟踪管理。项目中不写这个要被干，通过Pycharm commit会弹出一个窗口写message，很方便。

### 2.5 提交完后，再次`git status`查看一把:
>$ git status  
On branch master  
nothing to commit, working tree clean  

**以上，就完成了从初始化一个版本库，到创建文件，保存修改，再到提交代码的流程。**

### 2.6 修改`index.html`，再次执行`git status`，可以看到modified文件，代表当前修改未暂存staged。
>Changes not staged for commit:  
  (use "git add <file>..." to update what will be committed)  
  (use "git restore <file>..." to discard changes in working directory)  
        modified:   index.html  

### 2.7 将第6步的修改直接通过`git commit -m "First commit"`命令。将报
>no changes added to commit (use "git add" and/or "git commit -a")  

而通过`git commit -m "First commit" index.html`时，无需执行`git add index.html`，即可提交到版本库。

**小结**：  
**git提交分为两个步骤：**  
1. 暂存变更：git add，将新文件或修改添加到暂存区stage，也就是index中
2. 提交变更：git commit，提交暂存区中的改动，而不是物理文件目前的改动（未提到到暂存区的改动），提交到当前分支（版本库）。
3. 可以通过：`git commit -m "msg" filename` 或者 `git commit -m "msg" -a`,将暂存stash + 提交commit合为一步。

### 2.8 增补，git commit --amend：
**场景**：问题修改后，所有修改已经commit到版本库了，但是发现漏改了一个文件。因为项目严格要求一个问题应当只有一个commit，最多再多一个检视修改，即两次commit。怎办呢？  
`git commit --amend`。`--amend`后面什么都不写，默认将修改追加到最后一次commit中。比如遗漏了`about.html`文件，修改后执行`git add about.html;git commit --amend`，此时会弹出文件，让你补充message，直接i,增加补充信息后wq退出。
>$ git commit --amend  
[master e101a8b] Thrid commit,修改index.html文件 --amend 追加修改about.html1  
 Date: Fri May 13 22:40:17 2022 +0800  
 2 files changed, 2 insertions(+), 1 deletion(-)  
 create mode 100644 about.html  

### 2.9 查看每次commit的md5值，`git log`。   
`git log e101a8b9cf7`，指定md5时，查看指定某次提交的信息。

### 2.10 **查看差异**，`git diff`：
- `git diff`， 查看已被跟踪文件未暂存的修改（工作区）与暂存区之间的差异:  
- `git diff --cached`，查看被跟踪文件，暂存区与版本库之间的差异；
- `git diff HEAD`，查看被跟踪文件，工作区与上一次commit之间的差异，HEAD指代最后一次commit。**一定要练习试验**
>$ git diff --cached  
diff --git a/about.html b/about.html  
index 7bfdb71..eb55abd 100644  
--- a/about.html  
+++ b/about.html  
@@ -1 +1,3 @@  
-<html>about</html>  
+<html>about;  
+modify  
+</html>  

### 2.11 HEAD：
HEAD指代最后一次提交；`HEAD^`，指代上一次提交；`HEAD^^`,指代上上一次提交；查看前n次提交,索引从0开始：`HEAD~n`。例如`git log HEAD~3`


### 2.12、检出，`git checkout`。
从暂存区或某个commit，检出文件到工作区。例如，因为某个问题修改了一个文件，但是最后发现修改的文件有问题，需要恢复到修改前的文件重新修改，但是改动量太大了，手动恢复很麻烦，怎么办，git checkout。  
|命令|含义|  
|:-:|:-|  
|`git checkout`| 列出暂存区可以被检出的文件  
|`git checkout file`|从暂存区恢复文件(检出文件)到工作区，就是覆盖工作区的文件，可以指定检出的文件。git checkout不会清楚stage。  
|`git checkout commit file`| 检出某个commit的指定文件到**暂存区和工作区**。  
|`git checkout .`| 检出暂存区的所有文件到工作区。  

**例如**：  
>git checkout e101a8b9cf735c518e748c6378 about.html  
Updated 1 path from ee45251  

### 2.13 重置，`git reset`。
**这是回退操作**。  
|命令|含义|  
|:-:|:-|  
|`git reflog`| 显示commit的信息，只要HEAD发生变化，都可以通过这条命苦看到，相当于日志。  
|`git reset`|列出将被reset的文件。  
|`git reset [commit_id] file`| 重置指定文件的暂存区与指定commit一致，未给出commit默认和上一次commit一致，**工作区不影响**。**使用场景：比如，某一次问题修改commit后，发现有一个文件的修改与本问题无关，误commit了。则可以reset commit_id file,恢复这个文件的暂存区到前一个commit，然后再amend到提交的commit，而工作区的修改保持不变；如果工作区需要恢复，再通过`git checkout file`。**  
|`git reset commit_id`| （版本库操作）重置当前分支的HEAD为指定的commit，同时重置暂存区的所有文件，但工作区不变。  
|`git reset --hard [commit_id]`| （版本库操作）重置当前分支的HEAD为指定commit，未指定commit则默认为上一次commit，同时重置暂存区和工作区与指定commit一致。  
|`git reset --keep commit_id`| （版本库操作）重置当前HEAD为指定commit（相当于移动HEAD指针。可见，HEAD并不一定是最后一次提交），但保持暂存区和工作区不变。  
**例如**：  
>`echo "modify" > about.html`  
`git add about.html`  添加到暂存区  
`git reset about.html`  使用最后一次commit覆盖暂存区  
`git diff`  工作区不受影响，修改还在  
`cat about.html`  
`git add about.html`  再次将修改添加到暂存区  
`git reset --hard HEAD`  使用最后一次commit覆盖暂存区和工作区  
`cat about.html`  
`git diff`  工作区和暂存区都被覆盖，修改被清空无法找回。因此，需求开发中慎用，有可能一周的编码一键回到解放前。  

**又如**：从某一次commit退回about.html文件。回退后，`git diff`可以看到，暂存区已经回退，但工作区还在。  
>$ git reset e101a8b9cf735c5 about.html  
>$ git diff  
diff --git a/about.html b/about.html  
index 7bfdb71..df24fcc 100644  
--- a/about.html  
+++ b/about.html  
@@ -1 +1,4 @@  
-<html>about</html>  
+<html>about;  
+modify;  
+20220514;  
+</html>  


### 2.14 移动和删除。  
注意这些执行命令都相当于修改，必须commit才生效。  
|命令|含义|  
|:-:|:-|  
|`git mv src dest`| 改名，直接把改名的改动放入暂存区，相当于`git add`。  
|`git rm file`| 会同时在版本库和工作目录中删除文件，这是真删除，慎操作，用`git rm --cached`比较安全。  
|`git rm --cached file`| 蒋文件从暂存区转成未暂存，从版本库中删除，但不删除工作目录的该文件，即文件恢复成不追踪状态。  


### 2.15 push到远端库。
**需要说明的是**：通过`git remote add origin git@gitcode.net:your_name/test.git`命令，与远端仓库建立连接，这里的origin相当于一个标识符或者快捷方式，指代origin后面的远端链接，所以这个origin是可以用其他名字的，只是大家都习惯用origin了。  
首先，在本地根目录初始化一个本地的版本库（创建`.git文件夹`）：`git init`；  
然后：与远端库建立关联（需要先在远端库创建test项目），`git remote add origin git@gitcode.net:your_name/test.git`；  
再次：将所有要push到远端的文件加入暂存区stash并commit，`git add .;git commit -m "Initial commit"`；  
最后：推送到远端，`git push -u origin master`。  
