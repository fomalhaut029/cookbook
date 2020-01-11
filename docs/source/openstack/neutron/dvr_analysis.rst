.. _dvr_analysis:

################################
DVR模式下网络流量分析
################################

实验环境
==============
- 虚拟交换机采用 linuxbridge
- 租户网络模式：vxlan

DVR配置
========
我这里环境采用kolla部署,相关配置如下：
::

    enable_neutron_dvr: "yes"

docker生成后，各个配置文件如下：
::

    #l3_agent.ini
    [root@nanwan-e18-neutron1 ~]# cat /etc/kolla/neutron-l3-agent/l3_agent.ini 
    [DEFAULT]
    agent_mode = dvr_snat

    #neutron.conf 
    [root@nanwan-e18-neutron1 ~]# cat /etc/kolla/neutron-l3-agent/neutron.conf 
    [DEFAULT]
    router_distributed = True

实验环境1
=============
- 创建一个外部网络public1 10.182.0.0/24
- 创建一个vxlan网络demo-net 192.168.100.0/24
- 创建一个VR，指定public1作为其外部网络，并添加接口连接到demo-net网络
- 在demo-net网络下新建一个虚拟机demo1,ip为：192.168.100.50

如下图所示：

.. figure:: /_static/images/20200107_160126.png

构键完成后，我们来看看给个节点都新增哪些命名空间，
首先我们看下与VR相关的命名空间：

我们可以看到计算节点和网络节点上都新增了一个qrouter-cb64323b-56a8-40f4-a75d-9acc8c4ecc82的namespace,其中cb64323b-56a8-40f4-a75d-9acc8c4ecc82
为VR的ID

.. figure:: /_static/images/20200107_160036.png

我们在看下与demo-net网络相关的命名空间有那些：

.. figure:: /_static/images/20200107_160824.png

从上面可以看出，构建完成后openstack分别在nanwan-e17-compute1、nanwan-e18-neutron2、nanwan-e18-neutron3，这个三个节点上
都新增了一个qrouter-xxx的命名空间，并在nanwan-e18-neutron3上新增了一个snat-xxx的命名空间
同时在nanwan-e18-neutron2上新增了一个qdhcp-xxx的命名空间


我们看下与vr相关的namespace:

.. figure:: /_static/images/20200107_160432.png


可以看出计算节点和网络节点的router的namespace的配置是一样的，那么接下来。我们来查看具体的虚拟机的流量是
如何到达网关的也就是这里的router的namespace

我们将按照下面的思路来判断流量的走向

#. 我们从虚拟机192.168.100.50去ping网关地址10.199.100.1,虚拟机流量通过虚拟机的eth0发出

#. 通过在每个虚拟网络设备处抓包。判断流量是否经过

1.首先我们先查询出demo-net网络关联的所有端口，这些端口作为我们查询的条件进行过滤
::

    (bare) [root@kolla-ansible kolla]# openstack --os-project-name test --os-username test --os-password password port list --network demo-net
    +--------------------------------------+------+-------------------+--------------------------------------------------------------------------------+--------+
    | ID                                   | Name | MAC Address       | Fixed IP Addresses                                                             | Status |
    +--------------------------------------+------+-------------------+--------------------------------------------------------------------------------+--------+
    | 4de80f99-3b5e-4e8c-af1e-b8bcc5d22691 |      | fa:16:3e:7b:dc:72 | ip_address='192.168.100.2', subnet_id='07e1eaa9-992d-46f6-99d5-34dcc055558b'   | ACTIVE |
    | 9a6b957c-70fc-42eb-9a4e-7dfd8b9557a4 |      | fa:16:3e:70:93:80 | ip_address='192.168.100.1', subnet_id='07e1eaa9-992d-46f6-99d5-34dcc055558b'   | ACTIVE |
    | a136db2d-1585-4988-ae22-9535432a86fb |      | fa:16:3e:2a:42:b7 | ip_address='192.168.100.189', subnet_id='07e1eaa9-992d-46f6-99d5-34dcc055558b' | ACTIVE |
    | f60fa760-ee28-4dcf-bc91-23c8fbc39ffc |      | fa:16:3e:53:7d:29 | ip_address='192.168.100.50', subnet_id='07e1eaa9-992d-46f6-99d5-34dcc055558b'  | BUILD  |
    +--------------------------------------+------+-------------------+--------------------------------------------------------------------------------+--------+

.. figure:: /_static/images/20200107_180341.png

2.我们知道192.168.100.50就是我们虚拟机的eth0 ip 因此tapf60fa760-ee设备就是连接虚拟机eth0的设备

::

    我们也可以通过如下命令行获取tab设备名称
    (bare) [root@kolla-ansible ~]# openstack port list | grep 192.168.100.50 | cut -d \| -f 2
    f60fa760-ee28-4dcf-bc91-23c8fbc39ffc

通过上述结果。得出该虚拟机eth0连接的tap虚拟设备为：tapf60fa760-ee ,然后我们通过对tapf60fa760-ee抓包获取到icmp包

3. 查询tapf60fa760-ee 所在的计算节点
::

    (bare) [root@kolla-ansible kolla]# ansible op -m shell -a "ip a |grep tapf60fa760"
    [WARNING]: log file at /tmp/ansible/ansible.log is not writeable and we cannot create it, aborting

    nanwan-e17-compute1 | CHANGED | rc=0 >>
    183: tapf60fa760-ee: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq master brq80526879-78 state UNKNOWN group default qlen 1000

    nanwan-monitor43 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e17-compute2 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e17-compute3 | FAILED | rc=1 >>
    non-zero return code

    nanwan-monitor42 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-neutron2 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-neutron1 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-controller2 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-controller1 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-controller3 | FAILED | rc=1 >>
    non-zero return code

    nanwan-monitor41 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-neutron3 | FAILED | rc=1 >>
    non-zero return code

通过上述命令我们查询到tapf60fa760-ee 设备在nanwan-e17-compute1 节点上

3. 然后我们进一步查询tap虚拟设备关联的网桥设备
::

    #查看tap设备关联的网桥
    [root@nanwan-e17-compute1 ~]# ip a|grep tapf60fa760-ee
    183: tapf60fa760-ee: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq master brq80526879-78 state UNKNOWN group default qlen 1000
    
    #对tap设备进行抓包分析
    [root@nanwan-e17-compute1 ~]# tcpdump -i tapf60fa760-ee
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on tapf60fa760-ee, link-type EN10MB (Ethernet), capture size 262144 bytes
    16:31:47.046671 IP 192.168.100.50 > 192.168.100.1: ICMP echo request, id 43009, seq 1708, length 64
    16:31:47.046972 IP 192.168.100.1 > 192.168.100.50: ICMP echo reply, id 43009, seq 1708, length 64

    #对连接的网桥设备进行抓包分析
    [root@nanwan-e17-compute1 ~]# tcpdump -i brq80526879-78
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on brq80526879-78, link-type EN10MB (Ethernet), capture size 262144 bytes
    16:38:06.109811 IP 192.168.100.50 > 192.168.100.1: ICMP echo request, id 43009, seq 2087, length 64
    16:38:06.110103 IP 192.168.100.1 > 192.168.100.50: ICMP echo reply, id 43009, seq 2087, length 64

我们看到tapf60fa760-ee设备 连接到了brq80526879-78的网桥上(每个网络都会生成一个该网络的网桥设备命名规范
为brq+网络ID前缀)，然后我们分别对两个设备进行抓包分析，发现都获取到了icmp包

4. 接下来我们看看brq80526879-78网桥设备连接了哪些虚拟网络设备?
::

    [root@nanwan-e17-compute1 ~]# ip a|grep brq80526879-78
    182: brq80526879-78: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default qlen 1000
    183: tapf60fa760-ee: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq master brq80526879-78 state UNKNOWN group default qlen 1000
    184: tap9a6b957c-70@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UP group default qlen 1000
    185: vxlan-12548: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UNKNOWN group default qlen 1000

    #这里我们也可以通过brclt命令查看
    [root@nanwan-e17-compute1 ~]# docker exec -it -u 0 neutron_linuxbridge_agent brctl show brq80526879-78
    bridge name	bridge id		STP enabled	interfaces
    brq80526879-78		8000.068ce27f103b	no		tap9a6b957c-70
                                tapf60fa760-ee
                                vxlan-12548

可以看到连接了 **vxlan-12548**  、 **tapf60fa760-ee** 、**tap9a6b957c-70** 三个虚拟网络设备
- vxlan-12548 ：demo-net网络的vxlan隧道
- tapf60fa760-ee ：连接虚拟机的tap设备
- tap9a6b957c-70 ： 连接路由器的tap设备

我们分别在这三个设备上进行抓包分析：
::

    [root@nanwan-e17-compute1 ~]# tcpdump -i tap9a6b957c-70 -n
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on tap9a6b957c-70, link-type EN10MB (Ethernet), capture size 262144 bytes
    ^C
    0 packets captured
    0 packets received by filter
    0 packets dropped by kernel
    [root@nanwan-e17-compute1 ~]# tcpdump -i vxlan-12548 -n
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on vxlan-12548, link-type EN10MB (Ethernet), capture size 262144 bytes
    17:02:07.359610 IP 192.168.100.50 > 192.168.100.1: ICMP echo request, id 43009, seq 3528, length 64
    17:02:07.359832 IP 192.168.100.1 > 192.168.100.50: ICMP echo reply, id 43009, seq 3528, length 64

可以发现vxlan-12548 接口有收到icmp包。而tap9a6b957c-70并没有收到相应的包

我们继续来看看vxlan-12548 在哪些节点上存在
::

    (bare) [root@kolla-ansible kolla]# ansible op -m shell -a "ip a |grep vxlan-12548"
    [WARNING]: log file at /tmp/ansible/ansible.log is not writeable and we cannot create it, aborting

    nanwan-e17-compute1 | CHANGED | rc=0 >>
    185: vxlan-12548: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UNKNOWN group default qlen 1000

    nanwan-monitor43 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e17-compute3 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e17-compute2 | FAILED | rc=1 >>
    non-zero return code

    nanwan-monitor42 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-neutron2 | CHANGED | rc=0 >>
    94: vxlan-12548: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UNKNOWN group default qlen 1000

    nanwan-e18-neutron1 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-controller2 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-controller1 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-controller3 | FAILED | rc=1 >>
    non-zero return code

    nanwan-monitor41 | FAILED | rc=1 >>
    non-zero return code

    nanwan-e18-neutron3 | CHANGED | rc=0 >>
    89: vxlan-12548: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UNKNOWN group default qlen 1000


可以看出vxlan-12548 分别存在于 nanwan-e17-compute1 、nanwan-e18-neutron2 、
nanwan-e18-neutron3 三个节点上
然后我们分别登入到nanwan-e18-neutron2、nanwan-e18-neutron3 节点上对vxlan-12548 进行抓包
::

    #nanwan-e17-neutron3 节点
    [root@nanwan-e17-neutron3 ~]# tcpdump -i  vxlan-12548 -n icmp
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on vxlan-12548, link-type EN10MB (Ethernet), capture size 262144 bytes
    17:40:06.925801 IP 192.168.100.50 > 192.168.100.1: ICMP echo request, id 43265, seq 97, length 64
    17:40:06.926062 IP 192.168.100.1 > 192.168.100.50: ICMP echo reply, id 43265, seq 97, length 64

    #nanwan-e17-neutron2 节点
    [root@nanwan-e17-neutron2 ~]# tcpdump -i  vxlan-12548 -n icmp
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode

可以看出旨在nanwan-e17-neutron3节点上获取到icmp包，同时我们在nanwan-e17-neutron3节点上
看看网桥设备brq80526879-78抓包信息：
::

    [root@nanwan-e17-neutron3 ~]# tcpdump -i  brq80526879-78 -n icmp
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on brq80526879-78, link-type EN10MB (Ethernet), capture size 262144 bytes
    17:47:42.015171 IP 192.168.100.50 > 192.168.100.1: ICMP echo request, id 43265, seq 552, length 64
    17:47:42.015242 IP 192.168.100.1 > 192.168.100.50: ICMP echo reply, id 43265, seq 552, length 64

能抓到相应的包，然后我们看下nanwan-e17-neutron3 下的网桥brq80526879-78 连接了那些设备：
::

    [root@nanwan-e17-neutron3 ~]# ip a |grep brq80526879-78
    87: tap9a6b957c-70@if4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UP group default qlen 1000
    88: tapa136db2d-15@if4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UP group default qlen 1000
    89: vxlan-12548: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue master brq80526879-78 state UNKNOWN group default qlen 1000
    90: brq80526879-78: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default qlen 1000

可以看出 设备：tap9a6b957c-70、tapa136db2d-15 、vxlan-12548连接到了网桥上，我们来看看各个设备都连接什么


从上面可以看出：

通过上面的梳理,我们整理出如下的网络流量图

