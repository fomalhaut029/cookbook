.. _deploy_sphinx_readthedoc_github:


########################
使用 Sphinx + Readthedoc + GitHub 建立个人的博客
########################



.. note :: 

   一直都想准备搭建一个个人的知识库，方便自己总结归纳，原先一直是使用有道云笔记，但是
   都是比较的零散,看到apache cloudstack 的文档是使用Readthedoc,从风格看起来是我比较
   喜欢的。因此去了解一下是基于Sphinx + Readthedoc + GitHub来构建的。感觉挺不错的。
   因此我也打算基于这个来构建自己的知识库系统

.. contents:: 目录

..
   section-numbering::


--------------------------

========================
基本介绍
========================

-------------------------------
Sphinx
-------------------------------
Sphinx是一个工具，她能够轻易地创建智慧和优雅的文档，她是出自Georg Brandl之手，在BSD许可证下授权。

她最初是为了新版的python文档， 因此在python项目的文档具有完美的特性，但是同样支持c/c++，目前正在计划增加对其他的语言的支持。 理所当然，本页面也是使用Sphinx创造自reStructuredText格式源！Sphinx具有如下的特点：

输出格式： 

* 超文本标记语言 (包括Windows HTML帮助)，LaTeX (可打印的PDF版本)，手册页，纯文本
* 丰富的交叉引用： 语义标记以及针对函数，类，引用，词汇表（术语）和相似的信息块的自动链接
* 层次结构： 简单的文本树定义，就能自动地链接到同层（兄弟姐妹）、上一层（父母）以及下一层（子女）的文本位置
* 自动生成目录： 通用索引以及语言模块的目录
* 代码高亮： 代码自动高亮，通过使用 Pygments
* 扩展功能： 自动测试的代码片段，包括从Python模块（API文档）的文档字符串

Sphinx 使用 reStructuredText 作为标记语言, 可以享有 Docutils 为reStructuredText提供的分析，转换等多种工具.

-------------------------------
Readthedoc
-------------------------------

Read the Docs是一个在线文档托管服务，可以从各种版本控制系统中导入文档,
支持webhooks，当你提交代码时，文档将被自动构建。
Readthedocs支持Markdown格式和sphinx格式的文档排版，是部署项目文档的绝佳平台。
利用Github的托管服务，我们可以方便地将文档托管于Github，并利用Readthedocs查阅


========================
安装
========================

-------------------------------
环境及版本说明
-------------------------------
* Windows 10 企业版 1803
* Python 3.7.3
* pip 19.0.3

-------------------------------
安装Sphinx及组件
-------------------------------

1. 安装sphinx
::

    pip3 install sphinx

2. 安装完成后,我们创建一个文档目录，我这里创建一个cookbook目录
``D:\gitcode\cookbook``
并进入``cookbook``目录，启动
::

    sphinx-quickstart

3. 执行
``sphinx-quickstart`` 
后，按照向导提示选择,会生成make.bat脚本，方便后续直接使用生成html文档
::

    ./make html

最后会生成 Sphinx 一个文档项目必需的核心文件，包括：
::  

	│ make.bat
	│ Makefile
	├─build
	└─source
	　　│ conf.py
	　　│ index.rst
	　　├─_static
	　　└─_templates::

如果向导中的所有设置都保存在 conf.py 中，可以随时调整。

4. 安装支持mackdown的扩展
:: 

    pip3 install recommonmark

5. 安装完成后.需要在 
``config.py`` 
中配置
::

    extensions = ['recommonmark']


-------------------------------
配置GitHub
-------------------------------
1. 在github中创建一个repo

2. 将本地
``cookbook``
目录与远程目录关联
::

    git init
    git add README.md
    git commit -m "first commit"
    git remote add origin https://github.com/xxxxxxx/cookbook.git
    git push -u origin master

-------------------------------
配置Read The Docs
-------------------------------
1. 登入到
https://readthedocs.org/

2. 进入
``设置``  
在
``已连接的服务``
中选择 
``Connect to GitHub``

.. figure:: /_static/images/readthedoc1.png
   :scale: 100
   :align: center

3. 进入
``我的项目``
选择
``Import a Project``
选择github中创建的cookbook库

.. figure:: /_static/images/readthedoc2.png
   :scale: 100
   :align: center


| 这样我们就能通过构建。然后查看托管的文档了

.. figure:: /_static/images/readthedoc3.png
   :scale: 100
   :align: center

---------------------

参考文档：

.. [#] http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
.. [#] https://kyzhang.me/2018/05/08/Sphinx-Readthedocs-GitHub2build-wiki/

