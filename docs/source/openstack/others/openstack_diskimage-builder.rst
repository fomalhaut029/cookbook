
.. diskimage-builder:

############################
diskimage-builder之制作镜像
############################


.. tip:: 
   利用dib制作镜像

   此文档命令都是基于 ``openstack stein`` 版本 

.. contents:: 目录

..
   section-numbering::

--------------------------


diskimage-builder是openstack的官方项目，是cloudimage镜像的制作工具。学会用diskimage-builder我们就能定制属于我们自己云平台的镜像，前提是理解并会用里面的各种elements，这个需要时间多练习。

每个elements里面可以包含这些内容：

environment.d：定义环境变量

preinstall.d ：安装前准备工作，如定义镜像版本号

install.d ：安装过程中执行脚本

finalise.d root.d ：安装结束后执行脚本

element-deps  ：依赖的其他元素

element-provides：应该和系统有关，不太清楚
