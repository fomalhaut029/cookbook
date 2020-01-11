
.. _kolla_install:

####################################
Kolla & Kolla-ansible 部署 OpenStack 
####################################


.. contents:: 目录

..
   section-numbering::

--------------------------


部署环境 
=========

* 平台：VMware Workstations 
* 操作系统：CentOS 74，4C/6G 
* 双网卡 - [ ] Bridge
  模式：eth0 - [ ] Bridge 模式：eth1 - Kolla branch stable/qeuees 
* Kolla-ansible branch stable/qeuees - OpenStack branch stable/qeuees

配置网络
=========

::

    cat /etc/sysconfig/network-scripts/ifcfg-ens33
    TYPE=Ethernet
    PROXY_METHOD=none
    BROWSER_ONLY=no
    BOOTPROTO=dhcp
    DEFROUTE=yes
    IPV4_FAILURE_FATAL=no
    IPV6INIT=yes
    IPV6_AUTOCONF=yes
    IPV6_DEFROUTE=yes
    IPV6_FAILURE_FATAL=no
    IPV6_ADDR_GEN_MODE=stable-privacy
    NAME=ens33
    UUID=071505fd-62fa-4234-9ba8-d3958d678d09
    DEVICE=ens33
    ONBOOT=yes #修改为yes

配置本地存储 100G
======================

::

    pvcreate /dev/sdb
    vgcreate cinder-volumes /dev/sdb

配置pip加速源（阿里云）
==========================

::

    mkdir ~/.pip
    cat > ~/.pip/pip.conf << EOF 
    [global]
    trusted-host=mirrors.aliyun.com
    index-url=https://mirrors.aliyun.com/pypi/simple/
    EOF

配置yum加速源
=============

::

    yum install -y wget
    mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
    wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
    wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
    yum clean all
    yum makecache

配置代理
=============

::

    1.安装ss客户端
    pip install --upgrade pip
    pip install shadowsocks
    2.新建配置文件
    vi /etc/shadowsocks.json
    {
      "server":"x.x.x.x",             #你的 ss 服务器 ip
      "server_port":0,                #你的 ss 服务器端口
      "local_address": "127.0.0.1",   #本地ip
      "local_port":0,                 #本地端口
      "password":"password",          #连接 ss 密码
      "timeout":300,                  #等待超时
      "method":"aes-256-cfb",         #加密方式
      "workers": 1                    #工作线程数
    }
    我的配置为：
    {
      "server":"10.199.10.28",
      "server_port":3904,
      "local_address": "127.0.0.1",
      "local_port":1080,
      "password":"m17XaCZUS2cb5QxGs91op8QOIY",
      "timeout":300,
      "method":"aes-256-cfb",
      "workers": 1
    }

    3.启动

    nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &
    echo " nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &" /etc/rc.local   #设置自启动

    4.测试验证代理是否正常

    运行 curl --socks5 127.0.0.1:1080 http://httpbin.org/ip，如果返回你的 ss 服务器 ip 则测试成功：
    {
      "origin": "x.x.x.x"       #你的 ss 服务器 ip
    }
    5.安装Privoxy
    Shadowsocks 是一个 socket5 服务，我们需要使用 Privoxy 把流量转到 http／https 上。

    yum install -y privoxy

    6.修改配置文件
    vi /etc/privoxy/config
    listen-address 127.0.0.1:8118   # 8118 是默认端口，不用改，下面会用到
    forward-socks5t / 127.0.0.1:0 . # 这里的端口写 shadowsocks 的本地端口（注意最后那个 . 不要漏了）

    7.启动并添加到环境变量中
    systemctl restart privoxy

    vi /etc/profile
    在最后添加
    export http_proxy=http://127.0.0.1:8118       #这里的端口和上面 privoxy 中的保持一致
    export https_proxy=http://127.0.0.1:8118

    8.访问谷歌测试
    curl www.google.com.hk

    9.注意：
    如果不需要用代理了，记得把 /etc/profile 里的配置注释掉，不然会一直走代理流量。

配置docker 代理
================

::

    vi /etc/systemd/system/docker.service.d/http-proxy.conf
    [Service] 
    Environment="HTTP_PROXY=http://ip:port/"
    Environment="HTTPS_PROXY=http://ip:port/"

    systemctl daemon-reload && systemctl restart docker

配置防火墙
================

::

    systemctl stop firewalld
    systemctl disable firewalld
    yum install iptables -y
    yum install iptables-services -y
    systemctl start iptables.service
    systemctl enable iptables.service

    iptables -F
    iptables -P INPUT ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -P FORWARD ACCEPT
    service iptables save
    systemctl restart iptables.service

安装基础软件
================

::

    1. 安装docker
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    yum list docker-ce --showduplicates | sort -r
    yum makecache fast
    yum install docker-ce -y
    docker -version

    设置共享
    mkdir /etc/systemd/system/docker.service.d
    tee /etc/systemd/system/docker.service.d/kolla.conf << EOF
    [Service]
    MountFlags=shared
    EOF
    启动服务
    systemctl daemon-reload
    systemctl enable docker
    systemctl restart docker


    docker --version

    2.安装依赖包

    yum install -y python-devel libffi-devel gcc openssl-devel libselinux-python
    yum install -y python-pip git
    pip install -U pip
    pip install -U ansible
    pip install -U tox
    pip install -U python-openstackclient
    pip install -U docker
    pip install -U jinja2
    pip install -U ipaddres

     注意： 遇到
     ERROR: Cannot uninstall 'ipaddress'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall
     
     sudo pip install --ignore-installed ipaddress
     
    3. 时间同步
    systemctl enable ntpd.service && systemctl start ntpd.service && systemctl status ntpd.service

    4. 禁用selinux

    setenforce 0
    sed -i 's/SELINUX=enforcing/SELINUX=disabled' /etc/selinux/config 

    5.禁用宿主机的 Libvirt 服务(可忽略)
    systemctl stop libvirtd.service && systemctl disable libvirtd.service && systemctl status libvirtd.service

安装kolla(沙盒)
================

::

    virtualenv kolla_env
    source kolla_env/bin/activate

    git clone https://github.com/openstack/kolla -b stable/queens
    cd kolla
    pip install -r requirements.txt -r test-requirements.txt -e .

kolla-ansible(沙盒)
=====================

::

    virtualenv kolla-ansible_env
    source kolla-ansible_env/bin/activate

    cd ~/kolla
    git clone https://github.com/openstack/kolla-ansible -b stable/queens

    #安装依赖
    pip install -r requirements.txt -r test-requirements.txt -e .

    #创建 kolla 配置文件并设置权限
    sudo mkdir -p /etc/kolla
    sudo chown $USER:$USER /etc/kolla

    #拷贝 kolla 配置文件模版
    cp -r kolla-ansible/etc/kolla/* /etc/kolla 

    拷贝 ansible 主机清单文件
    cp kolla-ansible/ansible/inventory/* ～/kolla



修改配置文件
=====================

::

    修改koll 配置文件

    kolla_base_distro: "centos"

    kolla_install_type: "source"

    openstack_release: "rocky"

    network_interface: "eth0"

    neutron_external_interface: "eth1"

    kolla_internal_vip_address: "10.232.18.40" #訪問OpenStack的API

    nova_compute_virt_type: "qemu"

    enable_cinder_backend_lvm: "yes"
    enable_cinder: "yes"

    enable_trove: "yes"

    enable_haproxy: "no"

部署测试
========

制作部署脚本
++++++++++++++++++++

::

    cat > deploy.sh <<EOF
    #!/bin/bash
    set -uexv
    usage()
    {
        echo -e "usage : \n\$0 <action>"
        echo -e "  \$1 action"
    }
    if [ \$# -lt 1 ]; then
        usage
        exit 1
    fi
    /root/kolla/kolla-ansible/tools/kolla-ansible -i /root/kolla/all-in-one \$1
    EOF

    赋予执行权限
    chmod +x deploy.sh

部署OpenStack集群
++++++++++++++++++++

::

    ./deploy.sh bootstrap-servers
    ./deploy.sh prechecks
    ./deploy.sh pull
    ./deploy.sh deploy
    ./deploy.sh post-deploy
    //./deploy.sh "destroy --yes-i-really-really-mean-it"

附录
========

1. 模板登入定制密码脚本

   ::

       #!/bin/sh
       passwd root<<EOF
       wwwwww
       wwwwww
       EOF


