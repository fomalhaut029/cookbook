.. _linux_networt_debug:


###############################
Linux Birdge网络调试
###############################


.. contents:: 目录

..
   section-numbering::

--------------------------

环境描述
==========
#. 环境1：使用Linux Bridge 桥接网络

 * 双网卡 em1 ,em2

 * 双网桥 br1--em1 ,br2--em2

   ::

        [root@ironic-father ~]# ip a
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
            link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
            inet 127.0.0.1/8 scope host lo
            valid_lft forever preferred_lft forever
            inet6 ::1/128 scope host 
            valid_lft forever preferred_lft forever
        2: em1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br1 state UP group default qlen 1000
            link/ether 44:a8:42:0b:eb:53 brd ff:ff:ff:ff:ff:ff
            inet6 fe80::46a8:42ff:fe0b:eb53/64 scope link 
            valid_lft forever preferred_lft forever
        3: em2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br2 state UP group default qlen 1000
            link/ether 44:a8:42:0b:eb:54 brd ff:ff:ff:ff:ff:ff
        4: em3: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
            link/ether 44:a8:42:0b:eb:55 brd ff:ff:ff:ff:ff:ff
        5: em4: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
            link/ether 44:a8:42:0b:eb:56 brd ff:ff:ff:ff:ff:ff
        6: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
            link/ether 52:54:00:c3:4b:df brd ff:ff:ff:ff:ff:ff
            inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
            valid_lft forever preferred_lft forever
        7: virbr0-nic: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast master virbr0 state DOWN group default qlen 1000
            link/ether 52:54:00:c3:4b:df brd ff:ff:ff:ff:ff:ff
        9: br2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
            link/ether 44:a8:42:0b:eb:54 brd ff:ff:ff:ff:ff:ff
            inet6 fe80::bcf6:97ff:fedd:dda9/64 scope link 
            valid_lft forever preferred_lft forever
        10: br1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
            link/ether 44:a8:42:0b:eb:53 brd ff:ff:ff:ff:ff:ff
            inet 10.199.32.113/24 brd 10.199.32.255 scope global noprefixroute br1
            valid_lft forever preferred_lft forever
            inet6 fe80::46a8:42ff:fe0b:eb53/64 scope link 
            valid_lft forever preferred_lft forever
        25: vnet0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br2 state UNKNOWN group default qlen 1000
            link/ether fe:54:00:e7:be:b2 brd ff:ff:ff:ff:ff:ff
            inet6 fe80::fc54:ff:fee7:beb2/64 scope link 
            valid_lft forever preferred_lft forever

#. 环境2: openvswitch


抓包分析
========


创建一个dummy接口
++++++++++++++++++++
::

    ip link add name snooper0 type dummy
    ip link set dev snooper0 up

在Bridge中添加设备
++++++++++++++++++

Linux Bridge环境：
------------------
::  

    brctl addif  br2  snooper0
    #抓取icmp包
    tcpdump -i br2 -vv 'udp and port 67 and port 68' 

OpenvSwitch环境：
------------------
::

    #添加设备
    ip link add name snooper0 type dummy
    ip link set dev snooper0 up
    #绑定设备
    ovs-vsctl add-port br-int snooper0
    #镜像流量
    ovs-vsctl -- set Bridge br-int mirrors=@m  -- --id=@snooper0 \
    get Port snooper0  -- --id=@patch-tun get Port patch-tun \
    -- --id=@m create Mirror name=mymirror select-dst-port=@patch-tun \
    select-src-port=@patch-tun output-port=@snooper0 select_all=1
    #抓包
    tcpdump -i br2 -vv 'udp and port 67 and port 68' 

    #清理
    ovs-vsctl clear Bridge br-int mirrors
    ovs-vsctl del-port br-int snooper0
    ip link delete dev snooper0
















