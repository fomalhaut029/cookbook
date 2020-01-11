
.. _linux_vlan_config:

##########################################
linux网卡的vlan配置
##########################################

基本概念
==========

#. 物理网卡：物理网卡这里指的是服务器上实际的网络接口设备，在系统中可以看到的，比如2个物理网卡分别对应是eth0和eth1这两个网络接口。
#. 子网卡：子网卡在这里并不是实际上的网络接口设备，但是可以作为网络接口在系统中出现，如eth0:1、eth1:2这种网络接口。它们必须要依赖于物理网卡，虽然可以与物理网卡的网络接口同时在系统中存在并使用不同的IP地址，而且也拥有它们自己的网络接口配置文件。但是当所依赖的物理网卡不启用时（Down状态）这些子网卡也将一同不能工作。

 

#. 虚拟VLAN网卡：这些虚拟VLAN网卡也不是实际上的网络接口设备，也可以作为网络接口在系统中出现，
   但是与子网卡不同的是，他们没有自己的配置文件。他们只是通过将物理网加入不同的VLAN而生成的VLAN虚拟网卡。如果将一个物理网卡添加到多个VLAN当中去的话，就会有多个VLAN虚拟网卡出现，他们的信息以及相关的VLAN信息都是保存在/proc/net/vlan/config这个临时文件中的，而没有独自的配置文件。它们的网络接口名是eth0.1、eth1.2这种名字。

.. note:: 当需要启用VLAN虚拟网卡工作的时候，关联的物理网卡网络接口上必须没有IP地址的配置信息。

版权声明：本文为CSDN博主「stackpush」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/huakai_sun/article/details/82252264


安装工具包
===============
::

   yum install vconfig -y



环境检查
===========
::

   查看核心是否提供VLAN 功能
   [root@zx-120 neutron]# dmesg | grep -i 802
   [    1.485802] pci 0000:ff:02.5: [8086:2d95] type 00 class 0x060000
   [    1.497802] ACPI: bus type PNP registered
   [    1.498027] pnp 00:01: Plug and Play ACPI device, IDs PNP0b00 (active)

   查看系统内核是否支持802.1q协议
   [root@zx-120 neutron]# modprobe 8021q
   [root@zx-120 neutron]# lsmod |grep 8021q
   8021q                  33208  0 
   garp                   14384  1 8021q
   mrp                    18542  1 8021q


配置
=========
创建一个虚拟网卡并绑定到物理网卡em3上

::

   创建一个vlan虚拟网卡
   vconfig add em3 37

创建完成后,在 */proc/net/vlan/* 目录下会有em3.37 的网卡文件
当前配置只是临时生效。因此我们需要生成网卡配置文件，这样重启网络后就不会丢失vlan配置了
::

   cp ifcfg-em3 ifcfg-em3.37
   systemctl restart network

配置完成后，网卡文件配置如下：
::

   [root@zx-120 network-scripts]# cat ifcfg-em3
   TYPE=Ethernet
   BOOTPROTO=none
   DEFROUTE=yes
   NAME=em3
   UUID=466f5b69-1fd6-4261-ab5d-476d1fe403c6
   DEVICE=em3
   ONBOOT=yes


   [root@zx-120 network-scripts]# cat ifcfg-em3.37 
   VLAN=yes
   BOOTPROTO=none
   DEFROUTE=yes
   NAME=em3.37
   DEVICE=em3.37
   ONBOOT=yes

查看网卡配置情况：
::

   [root@zx-120 network-scripts]# ip a
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
         valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host 
         valid_lft forever preferred_lft forever
   2: em1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
      link/ether 14:fe:b5:da:a8:84 brd ff:ff:ff:ff:ff:ff
      inet 10.199.32.120/24 brd 10.199.32.255 scope global noprefixroute em1
         valid_lft forever preferred_lft forever
      inet6 fe80::42d5:9e2b:27bc:edb6/64 scope link noprefixroute 
         valid_lft forever preferred_lft forever
   3: em2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
      link/ether 14:fe:b5:da:a8:86 brd ff:ff:ff:ff:ff:ff
      inet 10.199.37.120/24 brd 10.199.37.255 scope global noprefixroute em2
         valid_lft forever preferred_lft forever
      inet6 fe80::16fe:b5ff:feda:a886/64 scope link 
         valid_lft forever preferred_lft forever
   4: em3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
      link/ether 14:fe:b5:da:a8:88 brd ff:ff:ff:ff:ff:ff
      inet6 fe80::16fe:b5ff:feda:a888/64 scope link 
         valid_lft forever preferred_lft forever
   5: em4: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
      link/ether 14:fe:b5:da:a8:8a brd ff:ff:ff:ff:ff:ff
   6: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
      link/ether 02:42:a9:94:84:73 brd ff:ff:ff:ff:ff:ff
      inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
         valid_lft forever preferred_lft forever
   7: em3.37@em3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
      link/ether 14:fe:b5:da:a8:88 brd ff:ff:ff:ff:ff:ff
      inet6 fe80::16fe:b5ff:feda:a888/64 scope link 
         valid_lft forever preferred_lft forever








