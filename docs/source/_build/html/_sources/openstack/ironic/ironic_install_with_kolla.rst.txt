.. _ironic_install_with_kolla:

#################################
通过kolla 安装Ironic 安装
#################################

本文介绍通过kolla来安装Ironic环境


.. contents:: 目录

..
   section-numbering::

--------------------------


环境说明
========
* CentOS Linux release 7.6.1810 (Core)
* openstack stein
* 双网卡 eth0 eth1: 网络配置如下：

.. note:: 注意这里的eth1 网卡必须是up状态，如果不是up状态，后续外部网络地址将无法与管理网络通信


eth0: 静态ip地址，作为管理地址
::

   [root@packstack network-scripts]# cat ifcfg-eth0
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
   NAME=eth0
   UUID=8d30e01b-299c-4db5-96ef-280dd53ac63a
   DEVICE=eth0
   ONBOOT=yes
   IPADDR=10.199.32.112
   NETMASK=255.255.255.0
   GATEWAY=10.199.32.1
   DNS1=114.114.114.114

eth1: 外部网络
::

   [root@packstack network-scripts]# cat ifcfg-eth1
   TYPE=Ethernet
   PROXY_METHOD=none
   BROWSER_ONLY=no
   BOOTPROTO=none
   DEFROUTE=yes
   IPV4_FAILURE_FATAL=no
   IPV6INIT=yes
   IPV6_AUTOCONF=yes
   IPV6_DEFROUTE=yes
   IPV6_FAILURE_FATAL=no
   IPV6_ADDR_GEN_MODE=stable-privacy
   NAME=eth1
   DEVICE=eth1
   ONBOOT=no

网卡状态：
::

   [root@packstack network-scripts]# ip a |grep state
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
   2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
   3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master ovs-system state UP group default qlen 1000


环境准备
========

关闭防火墙
+++++++++++++
::

   systemctl stop firewalld
   systemctl disable firewalld 

设置主机名称
+++++++++++++
::

   hostnamectl set-hostname kolla-ironic

关闭selinx ``/etc/selinux/config``
++++++++++++++++++++++++++++++++++++
::

   sed -i "s/^SELINUX=.*/SELINUX=disabled/g" /etc/selinux/config
   setenforce 0

   查看状态：

   cat /etc/selinux/config

   # This file controls the state of SELinux on the system.
   # SELINUX= can take one of these three values:
   #     enforcing - SELinux security policy is enforced.
   #     permissive - SELinux prints warnings instead of enforcing.
   #     disabled - No SELinux policy is loaded.
   SELINUX=disabled  #设置为disable
   # SELINUXTYPE= can take one of three values:
   #     targeted - Targeted processes are protected,
   #     minimum - Modification of targeted policy. Only selected processes are protected. 
   #     mls - Multi Level Security protection.
   SELINUXTYPE=targeted

4. 关闭NetworkManager(参考网络环境)
::

   systemctl disable NetworkManager
   systemctl stop NetworkManager
   systemctl enable network
   systemctl start network

安装kolla 环境
==============
略。请参照  :ref:`kolla 安装 <kolla_install>`


修改全局配置 ``global.yml``
===============================
::

   kolla_base_distro: "centos"
   kolla_install_type: "source"
   openstack_release: "stein"
   network_interface: "eth0"
   neutron_external_interface: "eth1"
   kolla_internal_vip_address: "10.199.32.112"
   enable_ironic: "yes"
   ironic_cleaning_network: "public"
   ironic_dnsmasq_dhcp_range: "10.199.32.20,10.199.32.25"
   openstack_logging_debug: "True"
   nova_compute_virt_type: "qemu"
   enable_haproxy: "no"

准备部署镜像和用户镜像
========================

.. note:: 

   ironic 整个部署流程中有两组映像，分别是 deploy 映像和 user 映像， 其中 deploy 映像用在 inspector 和 部署阶段， user 映像是用户需要安装的操作系统映像。
   制作ironic deploy镜像其实就是在普通镜像中添加一个ipa服务，用来裸机和ironic通信。 官方推荐制作镜像的工具有两个，分别是CoreOS tools和disk-image-builder 
   具体链接如下: https://docs.openstack.org/project-install-guide/baremetal/ocata/deploy-ramdisk.html
   我的环境中使用的是coreos的镜像。
   下载地址如下：http://tarballs.openstack.org/ironic-python-agent/coreos/files/

准备deploy镜像
+++++++++++++++++

::

   mkdir /etc/kolla/config/ironic/
   wget -O /etc/kolla/config/ironic/ironic-agent.kernel http://tarballs.openstack.org/ironic-python-agent/coreos/files/coreos_production_pxe-stable-stein.vmlinuz 
   wget -O /etc/kolla/config/ironic/ironic-agent.initramfs http://tarballs.openstack.org/ironic-python-agent/coreos/files/coreos_production_pxe_image-oem-stable-stein.cpio.gz

准备用户镜像
+++++++++++++++++

略。请参照  :ref:`DIB 制作镜像 <dib_make_ironic_agent>`

::

   disk-image-create centos7 baremetal dhcp-all-interfaces -o my-image
   mv my-image.* /opt/


安装openstack
==============
::
   
   

   #进入虚拟环境
   source /root/kolla-ansible_env/bin/activate

   cd /root/kolla-ansible/tools/
   ./kolla-ansible bootstrap-servers
   ./kolla-ansible prechecks
   ./kolla-ansible -vvvv deploy
   ./kolla-ansible -vvvv  post-deploy

配置openstack
================

初始化环境变量
+++++++++++++++++

:: 

   #初始化ironic节点ipmi信息(ip\端口\用户名\密码\pxe网卡mac地址也就是第一个网卡的mac地址)
   s1_ipmi_address=10.199.32.110
   s1_ipmi_port=6230
   s1_ipmi_username=admin
   s1_ipmi_password=password
   s1_nic_mac_address=00:1e:67:63:0b:58

   #初始化裸机节点的配置信息，注意一定要低于裸机节点的真实大小，我的裸机节点的真实大小为4C8G 20G硬盘
   RAM=2048
   DISK=18
   VCPUS=2
   HOST_CPU_ARCH=x86_64
   export IRONIC_API_VERSION=1.20

   #初始化neutron网络配置信息
   EXT_NET_CIDR='10.199.32.0/24'
   EXT_NET_RANGE='start=10.199.32.60,end=10.199.32.70'
   EXT_NET_GATEWAY='10.199.32.59'



ironic网络配置
+++++++++++++++++++++

::

   #创建网络：
   openstack network create --provider-physical-network physnet1 \
   --provider-network-type flat --share public

   #创建子网
   openstack subnet create  \
   --allocation-pool ${EXT_NET_RANGE} --network public \
   --subnet-range ${EXT_NET_CIDR} --gateway ${EXT_NET_GATEWAY} --dhcp  -- public-subnet

配置鏡像
++++++++++++++

::

   #上传裸机部署镜像
   openstack image create --disk-format aki --container-format aki --public \
   --file /etc/kolla/config/ironic/ironic-agent.kernel deploy-vmlinuz
   openstack image create --disk-format ari --container-format ari --public \
   --file /etc/kolla/config/ironic/ironic-agent.initramfs deploy-initrd

   #注册用户镜像
   glance image-create --name my-kernel --visibility public \
   --disk-format aki --container-format aki < /opt/my-image.vmlinuz

   glance image-create --name my-image.initrd --visibility public \
   --disk-format ari --container-format ari < /opt/my-image.initrd
   
   MY_VMLINUZ_UUID=$(glance image-list|grep my-kernel|awk -F "| " '{print $2}')
   MY_INITRD_UUID=$(glance image-list|grep my-image.initrd|awk -F "| " '{print $2}')

   glance image-create --name my-image --visibility public \
   --disk-format qcow2 --container-format bare --property \
   kernel_id=$MY_VMLINUZ_UUID --property \
   ramdisk_id=$MY_INITRD_UUID < /opt/my-image.qcow2

生成密钥对
++++++++++++++

::

   # 生成密钥对
   if [ ! -f ~/.ssh/id_rsa.pub ]; then
      echo Generating ssh key.
      ssh-keygen -t rsa -f ~/.ssh/id_rsa
   fi

   if [ -r ~/.ssh/id_rsa.pub ]; then
      echo Configuring nova public key and quotas.
      openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey
   fi

配置容量
++++++++++++++
::

   nova quota-class-update --instances 50 default
   nova quota-class-update --ram 5120000 default
   nova quota-class-update --cores 2000 default

创建裸金属实例的 Flavor
+++++++++++++++++++++++++++

.. note:: 
   
   在 Queen 版本中，Ironic 项目新增 Trait API，节点的 traits 信息可以注册到计算服务的 Placement API 中，用于创建虚拟机时的调度。添加 Trait API 后，注册到 Ironic 的裸机也可以通过 Trait API 注册到 Placement 资源清单中，最终支持裸机的部署调度。
   本文我们实践通过 Placement 来完成裸机的调度，通过 Resource Class 来标识 ironic node 的资源类型，通过 Resource Traits 来标识 ironic node 的特征，还可以通过 resources:VCPU=0、resources:MEMORY_MB=0、resources:DISK_GB=0 来 disable scheduling。
   ————————————————
   版权声明：本文为CSDN博主「范桂飓」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
   原文链接：https://blog.csdn.net/Jmilk/article/details/90107741

::

   nova flavor-create ai-bm-node1 1 ${RAM} ${DISK} ${VCPUS}
   nova flavor-key ai-bm-node1 set cpu_arch=x86_64
   nova flavor-key ai-bm-node1 set resources:CUSTOM_BAREMETAL_TEST=1
   nova flavor-key ai-bm-node1 set resources:VCPU=0
   nova flavor-key ai-bm-node1 set resources:MEMORY_MB=0
   nova flavor-key ai-bm-node1 set resources:DISK_GB=0

创建baremetal节点
++++++++++++++++++++++++

::

   openstack baremetal node create --driver ipmi --name node1

配置baremetal节点
++++++++++++++++++++++
::

   NODE1_UUID=$(openstack baremetal node list|grep node1 |awk -F "| " '{print $2}')

   #设置ipmi
   openstack baremetal node set $NODE1_UUID \
   --driver-info ipmi_username=$s1_ipmi_username \
   --driver-info ipmi_password=$s1_ipmi_password \
   --driver-info ipmi_address=$s1_ipmi_address \
   --driver-info ipmi_port=$s1_ipmi_port 

   #设置镜像
   DEPLOY_VMLINUZ_UUID=$(glance image-list|grep deploy-vmlinuz|awk -F "| " '{print $2}')
   DEPLOY_INITRD_UUID=$(glance image-list|grep deploy-initrd|awk -F "| " '{print $2}')

   openstack baremetal node set $NODE1_UUID \
   --driver-info deploy_kernel=$DEPLOY_VMLINUZ_UUID \
   --driver-info deploy_ramdisk=$DEPLOY_INITRD_UUID

   #设置规格
   openstack baremetal node set $NODE1_UUID \
   --property cpus=${VCPUS} \
   --property memory_mb=${RAM} \
   --property local_gb=${DISK} \
   --property cpu_arch=${HOST_CPU_ARCH}

   #设置资源标签(注意此处前面定义flavor的标签为：CUSTOM_BAREMETAL_TEST=1,这里要吧CUSTOM_前缀去掉)
   openstack --os-baremetal-api-version 1.21 baremetal node set $NODE1_UUID \
   --resource-class  BAREMETAL_TEST

   #设置端口信息
   openstack baremetal port create $s1_nic_mac_address --node $NODE1_UUID

   #配置状态
   1.将node状态转变为mangleable状态
   openstack baremetal node manage $NODE1_UUID
   2.将node节点转换成avaliable状态
   openstack baremetal node provide $NODE1_UUID

   openstack baremetal node list

通过virtualbmc生成虚拟ipmi设备
+++++++++++++++++++++++++++++++++++++++

略。请参照  :ref:`通过virtualbmc虚拟ipmi <virtualbmc_install>`

创建baremetal实例
+++++++++++++++++++++++++++++++++++++++
::
   
   openstack server create --image my-image --flavor ai-bm-node1  --key-name mykey --network public  node1


问题总结
=============

创建的flat网络不通
++++++++++++++++++++++

由于之前我们在配置物理环境中。eth1网卡并没有启动。y因此创建出来的flat 外部网络无法与物理网络通信，
因此只要启动eth1网卡即可
::

   ifup eth1
   #验证
   [root@packstack network-scripts]# ip netns exec qdhcp-c4e53fb0-d69c-4169-84e7-1e35187730c7 ping 10.199.32.1
   PING 10.199.32.1 (10.199.32.1) 56(84) bytes of data.
   64 bytes from 10.199.32.1: icmp_seq=1 ttl=255 time=1.46 ms
   64 bytes from 10.199.32.1: icmp_seq=2 ttl=255 time=0.945 ms
   64 bytes from 10.199.32.1: icmp_seq=3 ttl=255 time=3.12 ms

2. dhcp不通排查
++++++++++++++++++++++
查看日志：
:: 

   tail -f /var/log/kolla/neutron/dnsmasq.log
   正常应该为：一次dhcp应该包含以下4个过程
   Oct 14 23:54:08 dnsmasq-dhcp[126]: DHCPDISCOVER(tapf2ec7ee0-ec) fa:16:3e:e4:36:20 
   Oct 14 23:54:08 dnsmasq-dhcp[126]: DHCPOFFER(tapf2ec7ee0-ec) 10.199.32.28 fa:16:3e:e4:36:20 
   Oct 14 23:54:08 dnsmasq-dhcp[126]: DHCPREQUEST(tapf2ec7ee0-ec) 10.199.32.28 fa:16:3e:e4:36:20 
   Oct 14 23:54:08 dnsmasq-dhcp[126]: DHCPACK(tapf2ec7ee0-ec) 10.199.32.28 fa:16:3e:e4:36:20 host-10-199-32-28

抓包分析：
::

   在ironic节点抓取dhcp包
   tcpdump -i br1 -vv 'udp and port 67 and port 68'

   0.0.0.0.bootpc > 255.255.255.255.bootps: [udp sum ok] BOOTP/DHCP, Request from 52:54:00:af:43:5d
   10.199.32.26.bootps > 10.199.32.36.bootpc: [udp sum ok] BOOTP/DHCP, Reply, length 360, xid 0x55915542, secs 4, Flags [no
   0.0.0.0.bootpc > 255.255.255.255.bootps: [udp sum ok] BOOTP/DHCP, Request from 52:54:00:af:43:5d
   10.199.32.26.bootps > 10.199.32.36.bootpc: [udp sum ok] BOOTP/DHCP, Reply, length 360, xid 0x55915542, secs 10, Flag



















