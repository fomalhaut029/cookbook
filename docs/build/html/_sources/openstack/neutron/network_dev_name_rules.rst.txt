.. _network_dev_name_rules:

################################
openstack网络设备总结
################################

缩写解释
==============
* q=quantum 
* r=router
* g=gateway


相关概念
=========

- **bridge**

Bridge（桥）是 Linux 上用来做 TCP/IP 二层协议交换的设备,与现实环境中的HUB和二层交换机设备类似。
具体介绍请参考
:ref:`cloud_technology_linux_bridge`

- **openvswitch**

虚拟交换机,就如同它的名字一样，它是linux上通过软件是实现的交换机设备，具备硬件交换机的功能，目前
常用的虚拟机交换机主要为：linux bridge 和 openvswitch
具体介绍请参考
:ref:`cloud_technology_openvswitch`

- **tap-xxx**

模拟一个二层的网络设备，用于发送和接受二层网络数据包

- **tun-xxx**

模拟一个三层的网络设备，用于发送和接受三层数据包

- **veth**

虚拟的ethernet接口，以太网接口，通过以成对的形式出现，通常也称之为veth-pair,
一端发送的数据包会被另一端接受，因此这个设备通常用于连接各个虚拟设备，
比如两个namespace的连接，Bridge和OVS之间的连接，Docker容器之间的连接

- **qvb-xxx**

Neturon 的veth接口，用于linux Bridge 端

- **qvo-xxx**

Neturon 的veth接口，用于OVS 端

- **qr-xxx**


- **qg-xxx**

- **brq-xxx**

- **br-int**

OVS 下的内部网桥，也称为集成网桥,主要用于内部网络功能的网球
