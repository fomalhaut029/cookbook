
.. _cloud_technology_iptables:

##########################################
云计算-Iptables&Netfilter
##########################################

什么是Iptables/Netfilter?
============================
Iptables
+++++++++++++
* Iptables是Linux的"防火墙",这个是我们通常上的理解。其实Iptables并不是真正意义上的防火墙
  我们可以把它理解成一个防火墙的客户端软件。我们需要通过这个客户端软件去操作防火墙的相关
  功能。比如包过滤，转发等
* 工作在用户空间

Netfilter
+++++++++++++
* netfilter是linux内核中的一个数据包处理框架，用于替代原有的ipfwadm和ipchains等数据包处理程序
* 工作在内核空间

.. note:: Linux防火墙是通过netfiler这个内核框架实现，netfiler用于管理网络数据包。不仅具有网络地址转换(NAT)的功能，也具备数据包内容修改、以及数据包过滤等防火墙功能。利用运作于用户空间的应用软件，如iptables/firewalld/ebtables等来控制netfilter

Netfilter的基本原理
====================
原理图如下：它展示了netfilter框架在协议栈的位置,它可以清楚地看到netfilter框架是如何处理通过不同协议栈路径上的数据包

.. figure:: /_static/images/20191107_092318.png

解读：
 #. iptabels 用于处理ip数据包(IPv4 packet filter) / ebtables 处理以太网帧(修改源目的MAC等),
    工作于数据链路层 ``Link Layer``
 #. 有颜色的长方形方框代表iptables/ebtables的表和链

 #. 绿色的小方框表示 ``Network Layer`` 即iptbales的表和链

 #. 蓝色的小方框表示 ``Link Layer`` 即ebtables的表和链

 #. 椭圆形的方框 ``conntrack`` 即为connection tracking, 用于实现链接跟踪的功能，
    通过内核模块 **nf_conntrack** 实现

 #. ``bridge check`` 用于检查网络接口是否属于Bridge的某个port, 如果是就会处理Bridge的代码处理流程
    进入 ``Link Layer`` ,如果不是就会送到 网络层 ``Network Layer``

 #. ``bridging decision`` 类似于普通二层交换机的查表转发功能(MAC端口映射表)，根据mac地址判断是转发，
    还是交给上层协议处理.

    .. tip:: 我们可以通过在Bridge接口上抓包，来获取接口上所有的数据包。参考 

             :ref:`linux抓包分析 <linux_networt_debug>`
    

 #. ``routing decision`` 用于路由选择，根据系统的路由表 (ip route list| route -n)
    来决定是转发forward 还是本地处理

 #. 总结：**不同的包有不一样的路径，数据包总是从主机上的某一个接口进入，然后经过一系列的 
    ``check/decision/表链处理`` 
    到达主机中的某一个应用程序或者是主机中的某个接口发出，这里的接口既可以是物理网卡ethx 也可以是虚拟的网卡tun/vnex
    同时也可以是bridge的port**


.. note:: 复习一下TCP/IP四层模型的数据封装与解封过程

    .. figure:: /_static/images/20191107_100908.png


Iptabels的基本使用
====================

**iptables的结构：iptables -> Tables -> Chains -> Rules**

Iptabels的链 Chains
+++++++++++++++++++++

我们知道 **Netfilter** 在内核中协议栈中的不同位置实现了5个hook点(钩子函数),其他内核模块可以向
这些hook点注册处理函数，当数据包经过这些hook点的时候，在这些hook点上处理函数会一一的调用。

5个Chains：

* ``PREROUTING链`` :  处理刚到达本机并在路由转发前的数据包。它会转换数据包中的目标IP地址
  （destination ip address），通常用于DNAT(destination NAT)
* ``INPUT链`` ：处理输入数据包
* ``OUTPUT链`` ：处理输出数据包
* ``FORWARD链`` ：处理转发数据包,将数据转发到本机的其他网卡设备上
* ``POSTOUTING链`` ：处理即将离开本机的数据包。它会转换数据包中的源IP地址（source ip address），
  通常用于SNAT（source NAT）

.. figure:: /_static/images/20191107_120042.png


Iptables的表 Tables
+++++++++++++++++++++

我们把具有相同功能的规则放在一起，这样就形成了表的概念。也就是说，iptables中的表
就是具体特定功能的规则的集合

* ``filter表``：负责数据包过滤/拦截，可以包含INPUT、FORWARD、OUTPUT这3个内置chain,
  内核模块：iptable_filter
* ``nat表``：IP地址或端口号转换，可以包含PREROUTING、OUTPUT、POSTROUTING 
  3个内置chain，nat table在会话建立时会记录转换的对应关系，同一会话的回包和后续报文会自动地址转换，
  这是因为nat使用了ip_conntrack模块。，内核模块：iptable_nat
* ``mangle表``：拆解报文，用来修改IP报文，可以包含PREROUTING、OUTPUT、INPUT、FORWARD、POSTROUTING 
  5个内置chain 内核模块：iptable_mangle
* ``raw表``：负责过滤功能，内核模块：iptable_raw

.. figure:: /_static/images/20191107_141313.png

Iptables的规则 Rules
++++++++++++++++++++

语法：
iptables(选项)(参数)
::

    -t, --table table 对指定的表 table 进行操作， table 必须是 raw， nat，filter，mangle 中的一个。如果不指定此选项，默认的是 filter 表。

    # 通用匹配：源地址目标地址的匹配
    -p：指定要匹配的数据包协议类型；
    -s, --source [!] address[/mask] ：把指定的一个／一组地址作为源地址，按此规则进行过滤。当后面没有 mask 时，address 是一个地址，比如：192.168.1.1；当 mask 指定时，可以表示一组范围内的地址，比如：192.168.1.0/255.255.255.0。
    -d, --destination [!] address[/mask] ：地址格式同上，但这里是指定地址为目的地址，按此进行过滤。
    -i, --in-interface [!] <网络接口name> ：指定数据包的来自来自网络接口，比如最常见的 eth0 。注意：它只对 INPUT，FORWARD，PREROUTING 这三个链起作用。如果没有指定此选项， 说明可以来自任何一个网络接口。同前面类似，"!" 表示取反。
    -o, --out-interface [!] <网络接口name> ：指定数据包出去的网络接口。只对 OUTPUT，FORWARD，POSTROUTING 三个链起作用。

    # 查看管理命令
    -L, --list [chain] 列出链 chain 上面的所有规则，如果没有指定链，列出表上所有链的所有规则。

    # 规则管理命令
    -A, --append chain rule-specification 在指定链 chain 的末尾插入指定的规则，也就是说，这条规则会被放到最后，最后才会被执行。规则是由后面的匹配来指定。
    -I, --insert chain [rulenum] rule-specification 在链 chain 中的指定位置插入一条或多条规则。如果指定的规则号是1，则在链的头部插入。这也是默认的情况，如果没有指定规则号。
    -D, --delete chain rule-specification -D, --delete chain rulenum 在指定的链 chain 中删除一个或多个指定规则。
    -R num：Replays替换/修改第几条规则

    # 链管理命令（这都是立即生效的）
    -P, --policy chain target ：为指定的链 chain 设置策略 target。注意，只有内置的链才允许有策略，用户自定义的是不允许的。
    -F, --flush [chain] 清空指定链 chain 上面的所有规则。如果没有指定链，清空该表上所有链的所有规则。
    -N, --new-chain chain 用指定的名字创建一个新的链。
    -X, --delete-chain [chain] ：删除指定的链，这个链必须没有被其它任何规则引用，而且这条上必须没有任何规则。如果没有指定链名，则会删除该表中所有非内置的链。
    -E, --rename-chain old-chain new-chain ：用指定的新名字去重命名指定的链。这并不会对链内部照成任何影响。
    -Z, --zero [chain] ：把指定链，或者表中的所有链上的所有计数器清零。

    -j, --jump target <指定目标> ：即满足某条件时该执行什么样的动作。target 可以是内置的目标，比如 ACCEPT，也可以是用户自定义的链。
    -h：显示帮助信息；

**基本命令格式：**

iptables -t 表名 <-A/I/D/R> 规则链名 [规则号] <-i/o 网卡名> -p 协议名 <-s 源IP/源子网> --sport 源端口 <-d 目标IP/目标子网> --dport 目标端口 -j 动作







1.数据包在内核空间会有几种状态，但是映射到用户空间iptbales，就只用5种状态(注意这里说的状态不是tcp/ip协议中tcp连接的各种状态)：

===========   =====
状态            解释
===========   =====
NEW	            匹配连接的第一个包。意思就是，iptables从连接跟踪表中查到此包是某连接的第一个包。
                    判断此包是某连接的第一个包是依据conntrack当前"只看到一个方向数据包"([UNREPLIED])
                    不关联特定协议，因此NEW并不单指tcp连接的SYN包
ESTABLISHED     匹配连接的响应包及后续的包。意思是iptables从连接跟踪表中查到此包是
                属于一个已经收到响应的连接(即没有[UNREPLIED]字段)。因此在iptables状态中，
                只要发送并接到响应，连接就认为是ESTABLISHED的了。这个特点使iptables
                可以控制由谁发起的连接才可以通过，比如A与B通信，A发给B数据包属于NEW状态，
                B回复给A的数据包就变为ESTABLISHED状态。ICMP的错误和重定向等信息包也被看作是ESTABLISHED，
                只要它们是我们所发出的信息的应答。
RELATED         匹配那些属于RELATED连接的包，这句话说了跟没说一样。
                RELATED状态有点复杂，当一个连接与另一个已经是ESTABLISHED的连接有关时，
                这个连接就被认为是RELATED。这意味着，一个连接要想成为RELATED，
                必须首先有一个已经是ESTABLISHED的连接存在。这个ESTABLISHED连接再产生一个主连接之外的新连接，
                这个新连接就是RELATED状态了，当然首先conntrack模块要能”读懂”它是RELATED。拿ftp来说，
                FTP数据传输连接就是RELATED与先前已建立的FTP控制连接，
                还有通过IRC的DCC连接。有了RELATED这个状态，ICMP错误消息、FTP传输、DCC等才能穿过防火墙正常工作。
                有些依赖此机制的TCP协议和UDP协议非常复杂，
                他们的连接被封装在其它的TCP或UDP包的数据部分(可以了解下overlay/vxlan/gre)，
                这使得conntrack需要借助其它辅助模块才能正确”读懂”这些复杂数据包，
                比如nf_conntrack_ftp这个辅助模块
INVALID         匹配那些无法识别或没有任何状态的数据包。
                这可能是由于系统内存不足或收到不属于任何已知连接的ICMP错误消息。
                一般情况下我们应该DROP此类状态的包
UNTRACKED       状态比较简单，它匹配那些带有NOTRACK标签的数据包。需要注意的一点是，
                如果你在raw表中对某些数据包设置有NOTRACK标签，那上面的4种状态将无法匹配这样的数据包，
                因此你需要单独考虑NOTRACK包的放行规则
===========   =====

使用示例
==========


注意事项
=========

