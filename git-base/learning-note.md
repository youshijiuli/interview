# learning-note



## 1.为什么做版本控制

## 2.Git安装

Git 是一个开源的分布式版本控制软件,用以有效、高速的处理从很小到非常大的项目版本管理。 Git 最初是由*Linus Torvalds*设计开发的，用于管理Linux内核开发。Git 是根据GNU通用公共许可证版本2的条款分发的自由/免费软件，安装参见：[http://git-scm.com/](https://gitee.com/link?target=http%3A%2F%2Fgit-scm.com%2F)

GitHub是一个基于Git的远程文件托管平台（同GitCafe、BitBucket和GitLab等）。

Git本身完全可以做到版本控制，但其所有内容以及版本记录只能保存在本机，如果想要将文件内容以及版本记录同时保存在远程，则需要结合GitHub来使用。使用场景：

- 无GitHub：在本地 .git 文件夹内维护历时文件

- 有GitHub：在本地 .git 文件夹内维护历时文件，同时也将历时文件托管在远程仓库

其他：

集中式：远程服务器保存所有版本，用户客户端有某个版本 分布式：远程服务器保存所有版本，用户客户端有所有版本

## 3. 东北热创业史

首先在桌面有一个dbhot文件夹,里面是东北热的项目代码，如下所示：

![Ojwzb2lsno3nFHxMpaWcvAtlnAd.png](图片和附件/Ojwzb2lsno3nFHxMpaWcvAtlnAd.png)

界面大致是做一个样子：

写了一个月的成果如上所示，现在需要做版本控制，本质上就是使用Git管理文件夹；

步骤是这样的：

1.进入文件夹；

![LzxibZqSIoXXI3xR0U3ct478nPf.png](图片和附件/LzxibZqSIoXXI3xR0U3ct478nPf.png)

2.初始化

此时文件夹中多了一个`.git`文件夹；

查看当前状态：

红色表示文件未被管理，下面提交命令来管理；（README.txt）是新添加的；

3.管理

![OWYFbZ5XvoEqyrx9MrDcNhSwnbb.png](图片和附件/OWYFbZ5XvoEqyrx9MrDcNhSwnbb.png)

全部管理：git add .

4.生成版本 也就是提交

现在假设迭代一下：

修改一下index.html文件：

此时再来查看：

![VrCRbaM5IomouxxtfifcVSIKnEf.png](图片和附件/VrCRbaM5IomouxxtfifcVSIKnEf.png)

然后提交v2版本：

![IWApbue6iozIfMxoYL7cyfvLnzg.png](图片和附件/IWApbue6iozIfMxoYL7cyfvLnzg.png)

git log查看记录

git init 初始化

git add 管理这个文件

git add . 管理所有文件

由被管理状态 ---\> 生成版本的被管理状态

git commit -m 'v1' 生成版本

查看版本记录

git log

![MDVxb1Y8xoNjZzxTOuwcfKqXn1f.png](图片和附件/MDVxb1Y8xoNjZzxTOuwcfKqXn1f.png)

三个区域：

工作区：写代码

缓存区：

版本库：

第一阶段：单枪匹马自己干

第二阶段：模仿 什么热，什么火怎么做 短视频/直播

第三阶段：”约饭 “

> 因为是东北热 ，干倒东京热
> 
> 

如下所示：

```Plain Text
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body><li>亚洲</li><li>欧美</li><li>日韩</li><li>直播</li><li>约饭</li></body></html>
```

git查看：

上线了约饭功能，用户量陡增，但是被有关部门检测：你必须下架约饭功能，下架之后，我还让你上线；

那怎么办呢？代码不可能重写吧，很麻烦，所以代码回滚；

```Plain Text

```

如下：

![G39CbQilKoSruLxjSUWcQZUSnHh.png](图片和附件/G39CbQilKoSruLxjSUWcQZUSnHh.png)

查看代码：

![Tocrbywh9oCk6dx8fMQcwjhxnHc.png](图片和附件/Tocrbywh9oCk6dx8fMQcwjhxnHc.png)

现在盈利不够，在短视频阶段 一千万，但是约饭（擦边），一个亿

然后搞下作，然后让他上线约的功能，此约就是前面的约饭；

再次回滚；滚到约饭（通过种种手段）

![YQOkbVt7mo65C6xjifFc0R9TnPg.png](图片和附件/YQOkbVt7mo65C6xjifFc0R9TnPg.png)

git reflog 查看前面的版本

![OMoxbTZ93okU8jxT5GZcplgDn6c.png](图片和附件/OMoxbTZ93okU8jxT5GZcplgDn6c.png)

前滚：git reset --hard 版本号

页面效果如下：

#### 3.4 命令小总结

```Plain Text
git init
git add
git commit
git log
git reflog

git reset --hard 版本号
```

#### 3.5 商城功能\&bug修复

创建dev分支，开发商城功能：

![ER7QbGghqorSNyxj6rtctZ9wnSf.png](图片和附件/ER7QbGghqorSNyxj6rtctZ9wnSf.png)

```Plain Text
<body><li>亚洲</li><li>欧美</li><li>日韩</li><li>直播</li><li>约饭</li><li>商城50%</li></body></html>
```

此时提交第四个版本，V4,

现在出现了约饭功能出现了bug，怎么办？切换到master(此时代码就是v3的状态，因为V4实在dev分支开发的)，

![AI94bkKjSojYi3xaJr5c6ONunJf.png](图片和附件/AI94bkKjSojYi3xaJr5c6ONunJf.png)

但是在dev分支上是由的；

![S1uvb8dtuoBkkexvALVcGwmEnLe.png](图片和附件/S1uvb8dtuoBkkexvALVcGwmEnLe.png)

![FU1SbKQsAo5n0XxStO0cbazLnff.png](图片和附件/FU1SbKQsAo5n0XxStO0cbazLnff.png)

这里只是看下效果，咱们的bug还得解决呀，所以切换到master,创建bug分支：

![SvQzby0eOom9k6xkSF9cKSdCnMh.png](图片和附件/SvQzby0eOom9k6xkSF9cKSdCnMh.png)

切换到bug分支，修改代码（修改bug）:

![G1b0bvahbo75hexuv7Bc4pQ0nke.png](图片和附件/G1b0bvahbo75hexuv7Bc4pQ0nke.png)

bug修复完之后，我们此时还是在bug分支，现在需要切换到master分支，把bug分支代码合并到master分支；

![Y1cybtp46oTfzMxncM9c3W4PnHy.png](图片和附件/Y1cybtp46oTfzMxncM9c3W4PnHy.png)

bug合并玩之后，bug没什么用了，干掉它；

此时的页面：

![FztQb3DpSoxYf9xsa6cc9FcLnDg.png](图片和附件/FztQb3DpSoxYf9xsa6cc9FcLnDg.png)

在切换到dev,

![HhVZbOySroHCgcx5tpjcgNBunu3.png](图片和附件/HhVZbOySroHCgcx5tpjcgNBunu3.png)

继续开发商城功能；开发完毕，提交V6:

![KBnBb6d8hoc7DJxzddTc2wGhnff.png](图片和附件/KBnBb6d8hoc7DJxzddTc2wGhnff.png)

新功能开发完毕，切换到master,合并dev

![HSv4bsoE6oWHwnxuvgqczcW2n1c.png](图片和附件/HSv4bsoE6oWHwnxuvgqczcW2n1c.png)

发现产生了冲突：

![Ul0SbMThyozKq7xbRxOcrw4vncc.png](图片和附件/Ul0SbMThyozKq7xbRxOcrw4vncc.png)

手动解决冲突：

![Vvqwb3FFOoXptBxujGbc3wUmndg.png](图片和附件/Vvqwb3FFOoXptBxujGbc3wUmndg.png)

再次提交：

![P92LbEqfBoNqovxJJ8mcSWOwnXe.png](图片和附件/P92LbEqfBoNqovxJJ8mcSWOwnXe.png)

最终效果：

#### 3.6 bug修复总结

#### 3.7 工作流

git工作流

两个分支：

1个：master默认的 （只保留稳定的，线上的版本）

创建一个 dev分支 进行代码的开发

![ENkEbnqZMovju2xle39cyl8Lnvg.png](图片和附件/ENkEbnqZMovju2xle39cyl8Lnvg.png)

平台搭建完毕

公司想要探究不同业务

约饭 开发完成

现在想要开发商城功能（要开发2个月）

现在以及开发了一个月的时候，那个约饭的功能处bug了，这个时候怎么办

分支合并

两个分支A和B

如果要把A和并到B;

首先切换到B分支，（B） git merge A; 这样就把他合并到B;

要合并到谁，就在哪个分之上操作其他要被合并的分支

#### 3.8 进军三里屯

有钱了不就是造吗？买栋楼，买电脑

1.注册github账号

2.创建一个小仓库

3.本地代码推送到远程仓库（如果本地有v1,v2,v3,多个分支）都会推送到github的仓库

本地库推送到远程仓库：

![J5kEb2sBdohdpjxMgBTcbc7tnXc.png](图片和附件/J5kEb2sBdohdpjxMgBTcbc7tnXc.png)

如下所示：

![ArqubbR55otjGwxcU0mcqX9snF6.png](图片和附件/ArqubbR55otjGwxcU0mcqX9snF6.png)

但是发现没有推送dev分支；继续推送

![YGA0bIzcEobqvpxxBX5caLzqnOh.png](图片和附件/YGA0bIzcEobqvpxxBX5caLzqnOh.png)

效果：

![EhTqbEWJfo5cTwxLd7schC9inNu.png](图片和附件/EhTqbEWJfo5cTwxLd7schC9inNu.png)

假设很容易的推上去了，

现在到公司（三里屯）了，想要拉取代码

```Plain Text
git clone https://github.com/youshijiuli/dbhot.git
```

拉去下来了：

![UoxLbBXGFoN3hcxWrMjcM0qDn5S.png](图片和附件/UoxLbBXGFoN3hcxWrMjcM0qDn5S.png)

注意虽然只显示一个main分支，但是其实所有的都被克隆下来了：

![ChBSbh0DEo3R3OxVofwcQfnBnEc.png](图片和附件/ChBSbh0DEo3R3OxVofwcQfnBnEc.png)

#### 3.9 三点一线写代码

首秀按合并代码：

dev只有到v6:

把master合并到dev,使得dev能保持最新

开发代码：’

![Xe0zb7KrIoYn3Axpuuec8Kp9ngb.png](图片和附件/Xe0zb7KrIoYn3Axpuuec8Kp9ngb.png)

提交了代码，还要推送上去

现在下班坐地铁到家里，拉取代码：

![GrfnbOTiXohoXsx4Vxlc7At7npc.png](图片和附件/GrfnbOTiXohoXsx4Vxlc7At7npc.png)

在家开发了a2功能，推送上去：

![Rz9WbGvcboC0AYx7ev0c45P4ndg.png](图片和附件/Rz9WbGvcboC0AYx7ev0c45P4ndg.png)

第二天去三里屯，拉去代码：

![EGmRbXXZCoBQsNxUFmXc9AIhnxb.png](图片和附件/EGmRbXXZCoBQsNxUFmXc9AIhnxb.png)

然后就是循环往复，三点一线的干。

###### 三点一线总结：

初次在公司：

```Plain Text
ظᵇᬱᑕՙପդᎱ

 git clone ᬱᑕՙପ࣎ࣈ (ٖ᮱૪ਫሿ git remote add origin ᬱᑕՙପ࣎ࣈ)

ڔഘړඪ

 git checkout ړඪ
```

在公司下载玩代码，继续开发

```Plain Text

```

回到家继续写代码

```Plain Text

```

到公司继续写代码

```Plain Text

```

开发完毕，要上线：

```Plain Text

```

![SdPIbvotLouhZXxE8qHc0HeBnQc.png](图片和附件/SdPIbvotLouhZXxE8qHc0HeBnQc.png)

切换到dev,推送dev,因为之前是在main和并dev,再推送main,所以此时两者都是一样的，所以直接切换，然后推送即可；

![XqW5by3R0oUuscxVy38c7t4bnCd.png](图片和附件/XqW5by3R0oUuscxVy38c7t4bnCd.png)

此时dev,main都是最新的代码

然后回到家，更新代码：

![JpVUbi0R2oSabwxnmTOc6eSTnOg.png](图片和附件/JpVUbi0R2oSabwxnmTOc6eSTnOg.png)

此时不管在家还是公司都已经同步到了最新代码；

#### 3.10 约妹子忘记推送代码

再公司开发了a1.py

提交了，但是忘记推送远程仓库

![HcgabItaEorD5dx6VgscsrtinNd.png](图片和附件/HcgabItaEorD5dx6VgscsrtinNd.png)

回到家，拉取，但实际什么都没有，因为没有推送

![EkbqbiztgomCPex1UogcTg43nsb.png](图片和附件/EkbqbiztgomCPex1UogcTg43nsb.png)

然后写点别的功能，修改了a1.py,a2.py

然后提交推送 push

![AAitbOCNJoxJoqx43EbccgIlnRg.png](图片和附件/AAitbOCNJoxJoqx43EbccgIlnRg.png)

到公司，拉取，

![SK3AbmUSvoql2XxG9BZc2584ntR.png](图片和附件/SK3AbmUSvoql2XxG9BZc2584ntR.png)

发生冲突：

修改完成之后：

也就是冲突解决完成之后，在公司继续开发：

小补充

两个命令：

git pull origin

= git fetch origin dev \+ git merge origin/dev

见视频16

## 4. 多人协作开发

两大阶段

阶段一：自己在家写代码

阶段二：三点一线

现在进入第三阶段：

招人写代码，招了两个小弟，来写代码

![TpLDbmExTomfuAxELi4cfqmtnrh.png](图片和附件/TpLDbmExTomfuAxELi4cfqmtnrh.png)

面试题：怎么多人协作开发？

每个人有自己的分支，此分支都是从dev分支拆出来的；

review:代码检查

release:测试的分支（大公司很谨慎）

只有测试完成，才能合并到master ，也就是上线

bug修复再提交会dev,

辞旧岁gitflow工作流

#### 4.2 协作开发

方式一：先创建一个项目，然后邀请别人来协作开发；

![REitb0OAAoxiuRxpU7ZcqyqUn5g.png](图片和附件/REitb0OAAoxiuRxpU7ZcqyqUn5g.png)

方式二：创建一个组织，开源要求很多i人加入这个组织，也可以创建很多项目；

这个掏钱就不演示了；

现在一直都是版本，了解一下tag的使用；

打标签：

![WqMAbm4tkoxnZtxHJUecZKEAnAc.png](图片和附件/WqMAbm4tkoxnZtxHJUecZKEAnAc.png)

这个只是在本地，还要推送：

![TbuBbMHnno2DolxgbLecOc2onEh.png](图片和附件/TbuBbMHnno2DolxgbLecOc2onEh.png)

这时候看github:

![PRHkbzXyEoqh9LxrAfacP77GnMb.png](图片和附件/PRHkbzXyEoqh9LxrAfacP77GnMb.png)

现在两小弟也要开发，所以现在本地创建dev,推送到远程；

![NbCKbBCO6oyMypxbmnqcvbvAnwf.png](图片和附件/NbCKbBCO6oyMypxbmnqcvbvAnwf.png)

此时再github也会有dev,然后两个小弟注册账号，受邀加入组织；

项目或者组织都可以设置权限（读或者写）

小弟1------\> 斗地主分支

小弟2-------\> 炸金花

代码review和测试这里就暂时省略了；

## 5. 给开源项目贡献代码

1.fork源代码

相当于把比尔的源代码拷贝到自己的仓库

2.在自己的仓库修改代码

![LMZub3ajRoRNCbx6XoCcCZ7InkZ.png](图片和附件/LMZub3ajRoRNCbx6XoCcCZ7InkZ.png)

![Bx8Xbm5Xxo2dhUxB61Ac7UWTnDg.png](图片和附件/Bx8Xbm5Xxo2dhUxB61Ac7UWTnDg.png)

3.给源代码作者提交申请，（pull request）

如果别人同意就会，成功提交

巴豆精品 同步更新

[https://www.pianshen.com/article/22151496252/](https://gitee.com/link?target=https%3A%2F%2Fwww.pianshen.com%2Farticle%2F22151496252%2F)

## 6. 配置文件的三个位置

项目配置文件

.git/config

全局配置：

## 7. git免密登录

让git不在管理当前项目中的某些文件

```Plain Text
a.h
b.h
*.h
.gitignor
files/
```

去github搜索gitignore,

[https://github.com/github/gitignore](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fgithub%2Fgitignore)

## 8. 任务管理

- issures 文档以及任务管理

- wiki 项目文档说明

## 9. 一些拓展

分享一些使用过程中的问题

- 文件太大提交不了 不得超过50Mb(单文件)

- gitignore文件的使用

[https://blog.csdn.net/weixin_55252589/article/details/129017650](https://gitee.com/link?target=https%3A%2F%2Fblog.csdn.net%2Fweixin_55252589%2Farticle%2Fdetails%2F129017650)

