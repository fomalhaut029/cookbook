.. _proxmoxve_virtual_platform:

##########################################
Proxmox-VE搭配Ceph存储组建高可用虚拟化平台
##########################################


.. note:: 

    由于原先的测试平台服务器需要用于其他用途。所以考虑搭建新的测试平台。之前一直使用的是vmware或者是cloudstack。
    后面发现了proxmoxve .初步看了下感觉还不错。准备搭建一个尝试一下

.. contents:: 目录

..
   section-numbering::


--------------------------

前言
======

Proxmox VE (Proxmox Virtual Environment) 有方便易用的WEB界面，基于JAVA的UI和内核接口，
可以登录到VM客户方便的操作，还有易用的模板功能，基本跟老外的商业VPS环境差不多了，支持VT和ISCSI


环境说明
===============
* Proxmox VE  6.0-4
* Dell R720XD
* 两个千兆网卡

  * nic 1 access vlan 32 10.199.32.0/24
  * nic 2 trunk  vlan 100-150


安装配置
===============

更新源，将官方订阅源更改为非订阅版本 (注意版本。我这里是buster)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
::
    
    echo "#deb https://enterprise.proxmox.com/debian/pve buster pve-enterprise" > /etc/apt/sources.list.d/pve-enterprise.list
    echo "deb http://download.proxmox.com/debian/pve buster pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list 
    apt dist-upgrade

配置网络
++++++++++

安装配置ceph 存储
++++++++++++++++++++
