.. _virtualbmc_install:

#################################
virtualbmc 使用
#################################

本文介绍virtualbmc的使用



.. contents:: 目录

..
   section-numbering::

--------------------------


.... note:: 
   
   ©著作权归作者所有：来自51CTO博客作者757781091的原创作品
   ref :https://blog.51cto.com/penguintux/2103084


安装
===========

安装virtualbmc
+++++++++++++++++++

::

   yum install python-virtualenv
   virtualenv ven
   source ven/bin/activate
   pip install pip --upgrade

   yum install libvirt-devel gcc
   pip install virtualbmc


安装libvirt kvm，创建bridge
+++++++++++++++++++++++++++++
::

   yum install libvirt qemu-kvm
   yum install -y virt-install
   brctl addbr br1
   ifconfig br1 up

创建虚拟机
+++++++++++++++++++++++++++++

.. note:: 此处必须将iso文件移动到/tmp目录下。不然可能会有权限问题

::

   cp /root/CentOS-7-x86_64-Minimal-1810.iso /tmp/
   qemu-img create -f raw /opt/CentOS7.raw 20G
   virt-install --name centos7 --virt-type kvm --ram 2048 --cdrom=/tmp/CentOS-7-x86_64-Minimal-1810.iso --disk path=/opt/CentOS7-x86_64.raw --network bridge=br1 --graphics vnc,listen=0.0.0.0 --noautoconsole

启动vbmc
+++++++++++++++++++++++++++++
::

   vbmc add centos7 --port 6230 --username admin --password password
   验证：
   ipmitool -I lanplus -H 宿主机IP -U admin -P password -p 6230 power status







