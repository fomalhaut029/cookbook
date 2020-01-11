
.. _git_usage:

##########################################
Git 使用技巧
##########################################



安装配置
=========
略

Git基本使用
=============
::

    1.初始化新的仓库,进入项目根路径下
    #git init
    2.在远程仓库上创建项目,我这里使用的是 ``gitolite-admin``
    repo hmcloud
        RW+ = @admin
        R = @all
    3.关联远程仓库
    #git remote add origin git@10.200.3.100:hmcloud.git
    4.提交本地代码
    git add .
    git commit -m "初始导入"
    git push --set-upstream origin master

    5.我们在使用中将使用git flow的流程来处理



Git Flow的基本概念及使用
==========================
.. note:: 
    git作为代码版本管理软件的好处我们不用多说了，但是在使用git的过程中往往也会遇到一些问题：
    如果在git 管理过程中没有清晰的流程和规划，项目成员胡乱提交，到了项目后期代码版本会变得杂乱
    无章，项目会变得越来越难以维护，Git Flow的提出，很好的解决了这个问题。 下面我们通过一个项目
    实践一下git flow基本流程

Git Flow 分支
++++++++++++++++
.. note:: git flow 定义分支主要分为：

    **主要分支**: master,develop

    **支持分支**：feature,release,hostfix


**Master分支** 
    * master 分支是生产使用的分支,对应于线上的版本,
    * 版本发布后在此分支标记tag， 
    * 这个分支只能从其他分支合并，不能在这个分支直接修改

**Develop分支**
    * 开发的主要分支，
    * 主要包括下一个发布(release)版本的全部更改，该分支也被称作整合分支
    * 主要与feature分支合并，该分支代码为目前开发项目的最新代码

**Feature分支**
    * 用于开发一个新的功能的分支或者是长时间的任务开发工作
    * 基于develop分支创建
    * 功能开发完成后，最终会将feature分支合并到develop分支
    * 功能分支一般只存在于开发人员本地库中。不存在origin中，开发新功能时，我们一般从develop分支新建一个feature-xxx的功能分支
    * 命名规范：feature-*

**Release分支**
    * 用于发布一个新的版本
    * 基于develop分支创建
    * 完成发布后，将release分支合并到master和develop分支
    * 命名规范：release-*

**Hotfix分支**
    * 用于修复线上bug
    * 基于master分支创建
    * 完成修复后，必须合并到develop和master分支
    * 命名规范：hotfix-*


Git flow 使用流程
++++++++++++++++++++
构建主要分支
--------------

::

    1.初始化新的仓库,进入项目根路径下
    #git init
    2.在远程仓库上创建项目,我这里使用的是 ``gitolite-admin``
    repo hmcloud
        RW+ = @admin
        R = @all
    3.关联远程仓库
    #git remote add origin git@10.200.3.100:hmcloud.git
    4.提交本地代码
    git add .
    git commit -m "初始导入"
    git push --set-upstream origin master

创建develop分支
-----------------
::


















