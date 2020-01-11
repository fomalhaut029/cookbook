.. _virt_manager_kvm_vm:


###############################
使用virt_manager管理kvm虚拟机
###############################


.. contents:: 目录

..
   section-numbering::

--------------------------

基本介绍
=========

略

环境准备
=========
替换yum源
+++++++++++++
::

    yum install -y wget
    mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
    wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
    wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
    yum clean all
    yum makecache



安装kvm
========

检查cpu是否支持虚拟化    
+++++++++++++++++++++++++++

.. code-block:: console

    # grep vmx /proc/cpuinfo

    如果有对应的vmx输出，则说明cpu支持虚拟化

确保BIOS里开启虚拟化功能，即查看是否加载KVM模块
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: console

    [root@ironic ~]# lsmod | grep kvm
    kvm_intel             183621  0 
    kvm                   586948  1 kvm_intel
    irqbypass              13503  1 kvm

如果没有对应输出，则执行加载命令：

.. code-block:: console

    [root@kevin ~]# modprobe kvm
    [root@kevin ~]# modprobe kvm-intel

使用brctl配置桥接网络
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: console

    [root@ironic ~]# yum -y install bridge-utils qemu-kvm libvirt virt-install virt-manager bridge-utils
    [root@ironic ~]# systemctl restart network

编辑网卡文件 ``ifcfg-em1`` ``ifcfg-br1``：

ifcfg-br1

.. code-block:: console

    [root@ironic network-scripts]# cat ifcfg-br1 
    TYPE=Bridge
    PROXY_METHOD=none
    BROWSER_ONLY=no
    BOOTPROTO=none
    DEFROUTE=yes
    IPV4_FAILURE_FATAL=no
    NAME=br1
    DEVICE=br1
    ONBOOT=yes
    IPADDR=10.199.32.110
    NETMASK=255.255.255.0
    GATEWAY=10.199.32.1
    DNS1=114.114.114.114

ifcfg-em1 :

.. code-block:: console

    [root@ironic network-scripts]# cat ifcfg-em1 
    TYPE=Ethernet
    PROXY_METHOD=none
    BROWSER_ONLY=no
    BOOTPROTO=static
    DEFROUTE=yes
    IPV4_FAILURE_FATAL=no
    IPV6INIT=yes
    IPV6_AUTOCONF=yes
    IPV6_DEFROUTE=yes
    IPV6_FAILURE_FATAL=no
    IPV6_ADDR_GEN_MODE=stable-privacy
    NAME=em1
    UUID=a2cd110e-0a0d-4901-a136-dec936a38c34
    DEVICE=em1
    ONBOOT=yes
    BRIDGE=br1

重启网络：
++++++++++++++++++++++++++++++++++++++++++++++++++++++
.. code-block:: console

    [root@ironic network-scripts]# systemctl restart network


安装相关软件
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: console

    [root@ironic ~]# yum -y install libcanberra-gtk2 qemu-kvm libvirt

安装相关软件
++++++++++++++++++++++++++++++++++++++++++++++++++++++













