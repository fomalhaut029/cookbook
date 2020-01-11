
.. _install_muti_version_py_on_windows:

###############################
Windows 下安装多版本Python 环境
###############################


.. contents:: 目录

..
   section-numbering::

--------------------------

前言
================================

因为python 发展到version 3.x后,并不向下兼容，而目前很多的项目还是运行在python2.x版本中。因此
在同一个环境下会需要两个版本的运行环境。本文接下里将结束两种方式实现window下，python多版本的共存
问题


基本步骤
================================

一. 采用修改环境变量以及程序名称方式
++++++++++++++++++++++++++++++++++++

1. 安装python

我们到官网上下载两个版本的python 安装包，分别安装好 地址：https://www.python.org/downloads/


.. figure:: /_static/images/install_muti_version_py_on_windows1.png
   :scale: 100
   :align: center

我这边已经安装好了两个版本

.. figure:: /_static/images/install_muti_version_py_on_windows2.png
   :scale: 100
   :align: center


安装完成后。我们看下两个版本目录下的可执行文件：

.. figure:: /_static/images/install_muti_version_py_on_windows3.png
   :scale: 100
   :align: center

.. note:: 安装多个版本的方法就是避免变量重名的情况，比如python2.x和python3.x版本安装完毕后都有默认的python执行脚本和一个pip的脚本，我们只需要在path环境中让他们找到各自的脚本名称就可以轻松实现多版本安装啦！

2. 修改文件名称

.. figure:: /_static/images/install_muti_version_py_on_windows4.png
   :scale: 100
   :align: center

.. figure:: /_static/images/install_muti_version_py_on_windows5.png
   :scale: 100
   :align: center

同理，在python3安装目录下也执行同样的操作


3. 修改环境变量
将python2 和python3 都添加到系统环境变量中：

.. figure:: /_static/images/install_muti_version_py_on_windows6.png
   :scale: 100
   :align: center

4. 这样我们在系统中就可以通过python2 python3 来执行对应版本的命令了


.. figure:: /_static/images/install_muti_version_py_on_windows7.png
   :scale: 100
   :align: center

采用python 自带的launcher来切换 【推荐】
++++++++++++++++++++++++++++++++++++++++++++

.. note:: Python launcher是用于Windows中的一个实用程序，可帮助我们定位和执行不同版本的Python解释器。它允许脚本或者命令行指示特定的Python版本的首选项
    也就是说他能自动的选择你指定的解释器来执行py脚本。
    Python launcher 是3.3版本新增功能适用于 Windows 的 Python 启动器是一个实用组件，可帮助您定位和执行不同的 Python 版本。
    它允许脚本（或命令行）为特定的 Python 版本指示首选项，定位并执行该版本。

安装
------

.. figure:: /_static/images/install_muti_version_py_on_windows8.png
   :scale: 100
   :align: center

使用
------

    我们通过 py -2 、-3这样来指定使用不同的版本

.. figure:: /_static/images/install_muti_version_py_on_windows9.png
   :scale: 100
   :align: center







