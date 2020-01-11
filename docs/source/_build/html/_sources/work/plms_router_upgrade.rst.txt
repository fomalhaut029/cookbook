.. _plms_router_upgrade:

需求
=======
#. CIDR:172.21.72.0/21
#. 每个现法一个网段，总共8个现法 172.21.72.0~172.21.79.0
#. 每个现法可以互联
#. 可以通过acl控制访问

现状
=====
#. 目前专属云只有一个vpc CIDR : 172.21.72.0/21 已经创建了如下子网段：

| 172.21.72.33/28
| 172.21.72.33/28
| 172.21.72.1/30 
| 172.21.72.5/30 
| 172.21.72.9/30 
| 172.21.72.13/30
| 172.21.72.29/30
| 172.21.72.81/29
| 172.21.72.49/29
| 172.21.72.57/29
| 172.21.72.65/29
| 172.21.72.73/29
| 172.21.72.21/30
| 172.21.72.133/30
| 172.21.72.137/30
| 172.21.72.141/30
| 172.21.72.145/28
| 172.21.72.89/29 
| 172.21.72.97/29  

由于一个vpc下只能挂载24个网卡。那么意味着除去系统必须的eth0(本地链路)、eth1(外网网卡)、eth2(私有网关)，
那么一个vpc下可用的子网段就只能为24-3=21个
因此必须进行扩充

方案1
======
采用多vpc方案。vpc间通过vpn隧道互联,那么设计3个vpc 建立3条vpn隧道 每个vpc 部署三个子网。
那么刚好可以涵盖

优点：通过现有的架构即可实现,可以通过acs的api接口操作。不需要手动执行命令
缺点：扩充后。vpn隧道会指数增加，比如由3个扩充到4个，那么要新增3个vpc隧道

方案2
========
每个子网一个vpc。然后将每个vpc 挂载一个网络接口到一个虚拟机上，这个虚拟机充当路由器的作用，拓扑图如下：


目前的拓扑图




替换网关迁移步骤：
1. 在PRMS VPC下新建一个互联子网交换机原则上使用172.21.72.253 255.255.255.252 
. 删除现有私有网关(导出静态路由)
2. 新建L2网络 vlan: 306
3. 新建路由云主机：配置静态ip地址：172.21.71.1 ，并开启路由转发
echo "1" > /proc/sys/net/ipv4/ip_forward
echo "net.ipv4.ip_forward = 1" >>/etc/sysctl.conf
4. 测试路由云主机与172.21.71.2连通性,连通性正常
ping 172.21.71.2
 



::
    
    #路由主机设备添加
    ip route add 172.32.0.0/16 via 172.21.72.253   dev eth2   
    ip route add 192.168.0.0/16	 via 172.21.72.253 dev eth2
    ip route add 172.24.0.0/13	 via 172.21.72.253 dev eth2
    ip route add 172.22.0.0/15	 via 172.21.72.253 dev eth2
    ip route add 172.21.128.0/17 via 172.21.72.253 dev eth2
    ip route add 172.21.96.0/19	 via 172.21.72.253 dev eth2
    ip route add 172.21.80.0/20	 via 172.21.72.253 dev eth2
    ip route add 172.21.70.0/24	 via 172.21.72.253 dev eth2
    ip route add 172.21.68.0/23	 via 172.21.72.253 dev eth2
    ip route add 172.21.64.0/22	 via 172.21.72.253 dev eth2
    ip route add 172.21.0.0/18	 via 172.21.72.253 dev eth2
    ip route add 172.20.0.0/16	 via 172.21.72.253 dev eth2
    ip route add 172.16.0.0/14	 via 172.21.72.253 dev eth2

    ip route add 172.21.71.0/24 via 172.21.72.253  ####172.21.71.1在172.21.72.0/24所在vpc网络下，英寸去往71段的都指向72.253
    ip route add 172.21.72.0/24 via 172.21.72.253
    ip route add 172.21.73.0/24 via 172.21.73.253
    ip route add 172.21.74.0/24 via 172.21.74.253
    ip route add 172.21.75.0/24 via 172.21.75.253
    ip route add 172.21.76.0/24 via 172.21.76.253
    ip route add 172.21.77.0/24 via 172.21.77.253
    ip route add 172.21.78.0/24 via 172.21.78.253
    ip route add 172.21.79.0/24 via 172.21.79.253


    #每个vpc路由 比如在72网段的路由器上添加以下静态路由，其他网段同理
    ip route add 172.21.73.0/24 via 172.21.72.254
    ip route add 172.21.74.0/24 via 172.21.72.254
    ip route add 172.21.75.0/24 via 172.21.72.254
    ip route add 172.21.76.0/24 via 172.21.72.254
    ip route add 172.21.77.0/24 via 172.21.72.254
    ip route add 172.21.78.0/24 via 172.21.72.254
    ip route add 172.21.79.0/24 via 172.21.72.254



    #上海现法：172.21.79.0/24 宿主机Prms_computel21
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.1.31 "
    ip route add 172.21.71.0/24 via 172.21.79.254
    ip route add 172.21.72.0/24 via 172.21.79.254
    ip route add 172.21.73.0/24 via 172.21.79.254
    ip route add 172.21.74.0/24 via 172.21.79.254
    ip route add 172.21.75.0/24 via 172.21.79.254
    ip route add 172.21.76.0/24 via 172.21.79.254
    ip route add 172.21.77.0/24 via 172.21.79.254
    ip route add 172.21.78.0/24 via 172.21.79.254
    ip route list
    "

    #武汉现法：172.21.78.0/24 宿主机Prms_computel21
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.0.83 "
    ip route add 172.21.71.0/24 via 172.21.78.254
    ip route add 172.21.72.0/24 via 172.21.78.254
    ip route add 172.21.73.0/24 via 172.21.78.254
    ip route add 172.21.74.0/24 via 172.21.78.254
    ip route add 172.21.75.0/24 via 172.21.78.254
    ip route add 172.21.76.0/24 via 172.21.78.254
    ip route add 172.21.77.0/24 via 172.21.78.254
    ip route add 172.21.79.0/24 via 172.21.78.254
    ip route list
    "


    #成都现法：172.21.77.0/24 宿主机Prms_computel23
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.3.3 "
    ip route add 172.21.71.0/24 via 172.21.77.254
    ip route add 172.21.72.0/24 via 172.21.77.254
    ip route add 172.21.73.0/24 via 172.21.77.254
    ip route add 172.21.74.0/24 via 172.21.77.254
    ip route add 172.21.75.0/24 via 172.21.77.254
    ip route add 172.21.76.0/24 via 172.21.77.254
    ip route add 172.21.78.0/24 via 172.21.77.254
    ip route add 172.21.79.0/24 via 172.21.77.254
    ip route list
    "


    #重庆现法：172.21.76.0/24 宿主机Prms_SSD_computel43
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.0.21 "
    ip route add 172.21.71.0/24 via 172.21.76.254
    ip route add 172.21.72.0/24 via 172.21.76.254
    ip route add 172.21.73.0/24 via 172.21.76.254
    ip route add 172.21.74.0/24 via 172.21.76.254
    ip route add 172.21.75.0/24 via 172.21.76.254
    ip route add 172.21.77.0/24 via 172.21.76.254
    ip route add 172.21.78.0/24 via 172.21.76.254
    ip route add 172.21.79.0/24 via 172.21.76.254
    ip route list
    "

    #天津现法：172.21.75.0/24 宿主机Prms_SSD_computel43
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.3.150 "
    ip route add 172.21.71.0/24 via 172.21.75.254
    ip route add 172.21.72.0/24 via 172.21.75.254
    ip route add 172.21.73.0/24 via 172.21.75.254
    ip route add 172.21.74.0/24 via 172.21.75.254
    ip route add 172.21.76.0/24 via 172.21.75.254
    ip route add 172.21.77.0/24 via 172.21.75.254
    ip route add 172.21.78.0/24 via 172.21.75.254
    ip route add 172.21.79.0/24 via 172.21.75.254
    ip route list
    "

    #沈阳现法：172.21.74.0/24 宿主机Prms_SSD_computel41
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.3.246 "
    ip route add 172.21.71.0/24 via 172.21.74.254
    ip route add 172.21.72.0/24 via 172.21.74.254
    ip route add 172.21.73.0/24 via 172.21.74.254
    ip route add 172.21.75.0/24 via 172.21.74.254
    ip route add 172.21.76.0/24 via 172.21.74.254
    ip route add 172.21.77.0/24 via 172.21.74.254
    ip route add 172.21.78.0/24 via 172.21.74.254
    ip route add 172.21.79.0/24 via 172.21.74.254
    ip route list
    "

    #深圳现法：172.21.73.0/24 宿主机Prms_SSD_computel41
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.2.45 "
    ip route add 172.21.71.0/24 via 172.21.73.254
    ip route add 172.21.72.0/24 via 172.21.73.254
    ip route add 172.21.74.0/24 via 172.21.73.254
    ip route add 172.21.75.0/24 via 172.21.73.254
    ip route add 172.21.76.0/24 via 172.21.73.254
    ip route add 172.21.77.0/24 via 172.21.73.254
    ip route add 172.21.78.0/24 via 172.21.73.254
    ip route add 172.21.79.0/24 via 172.21.73.254
    ip route list
    "

    #深圳事务中心：172.21.72.0/24 宿主机Prms_computel23
    ssh -i /root/.ssh/id_rsa.cloud -p 3922 169.254.3.241 "
    ip route add 172.21.73.0/24 via 172.21.72.254
    ip route add 172.21.74.0/24 via 172.21.72.254
    ip route add 172.21.75.0/24 via 172.21.72.254
    ip route add 172.21.76.0/24 via 172.21.72.254
    ip route add 172.21.77.0/24 via 172.21.72.254
    ip route add 172.21.78.0/24 via 172.21.72.254
    ip route add 172.21.79.0/24 via 172.21.72.254
    ip route list
    "





    
    ##################prms 现有vpc下的子网交换机：
    172.21.72.33/28
    172.21.72.33/28
    172.21.72.1/30 
    172.21.72.5/30 
    172.21.72.9/30 
    172.21.72.13/30
    172.21.72.29/30
    172.21.72.81/29
    172.21.72.49/29
    172.21.72.57/29
    172.21.72.65/29
    172.21.72.73/29
    172.21.72.21/30
    172.21.72.133/30
    172.21.72.137/30
    172.21.72.141/30
    172.21.72.145/28
    172.21.72.89/29 
    172.21.72.97/29 


    每个vpc下需要执行一下补丁程序
    登入到vpc的vr下执行：
    cp /opt/cloud/bin/configure.py /opt/cloud/bin/configure.py.bak
    sed -i '266d' /opt/cloud/bin/configure.py
    sed -i '262d' /opt/cloud/bin/configure.py
    sed -i '261a\                logging.info("#####################################@%s",rule["destcidr"])' /opt/cloud/bin/configure.py
    sed -i '262a\                if "destcidr" in rule.keys():' /opt/cloud/bin/configure.py
    sed -i '263a\                    self.ingressdest = rule["destcidr"]' /opt/cloud/bin/configure.py
    sed -i '264a\                else:' /opt/cloud/bin/configure.py
    sed -i '265a\                    self.ingressdest = "0.0.0.0/0"' /opt/cloud/bin/configure.py
    sed -i '266a\                if self.ingressdest.strip()=="":' /opt/cloud/bin/configure.py
    sed -i '267a\                    self.ingressdest = "0.0.0.0/0"' /opt/cloud/bin/configure.py
    sed -i '268a\                self.dest = "-s %s -d %s" % (rule["cidr"],self.ingressdest)' /opt/cloud/bin/configure.py
    sed -i '272a\                    self.dest = "-d %s -s %s" % (rule["cidr"],self.ingressdest)' /opt/cloud/bin/configure.py



