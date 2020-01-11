
.. _configure_ubuntu_develoy_env:

##########################################
使用ubuntu作为开发环境
##########################################

安装
==========
略

.. note:: 
   
   使用U盘制作启动盘。然后修改bios,直接安装就行了。由于我是在已有的window系统的
   下的电脑下安装双系统。安装完成后遇到ubuntu找不到启动引导的问题。解决方案如下：
   :: 
       
       1.重新使用U盘进入到ubuntu的live cd系统，
       2. 打开terminal，添加boot-repair的ppa源：sudo add-apt-repository ppa:yannubuntu/boot-repair
       3. sudo apt-get update
       4. sudo apt-get install boot-repair
       5. sudo boot-repair
       6. 在打开的窗口中选择引导安装的位置，点击应用即可修复

优化
=====
更新apt源
+++++++++
::

   sudo echo >/etc/apt/sources.list

   tee /etc/apt/sources.list << EOF
   deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
   EOF

   sudo apt-get update

安装相关工具
++++++++++++
.. note:: `我们这里参考这个哥们的文档进行配置 <https://github.com/int32bit/dotfiles>`_ https://github.com/int32bit/dotfiles






遇到的问题
============
浏览器没有声音
++++++++++++++
::
   
   fa

vi下方向键变成字母
+++++++++++++++++++++
::

   sudo apt-get remove vim-common（卸载系统自带的vi编辑器）
   sudo apt-get install vim



















