
.. _openstack-dib_make_ironic-agent:


####################
DIB制作ironic镜像
####################



.. contents:: 目录

..
   section-numbering::

--------------------------

环境描述
=============================

- CentOS Linux release 7.4.1708 (Core)


安装
=============================

替换yum以及epel源
----------------------------

::  

    mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup #备份 
    curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo  #下载阿里云源
    yum clean all && yum makecache

    mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup
    mv /etc/yum.repos.d/epel-testing.repo /etc/yum.repos.d/epel-testing.repo.backup
    yum install -y wget
    wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

替换pip源
++++++++++++++++++++++

::

    mkdir ~/.pip
    cat > ~/.pip/pip.conf << EOF
    [global]
    trusted-host=mirrors.aliyun.com
    index-url=https://mirrors.aliyun.com/pypi/simple/
    EOF

安装相关软件包
++++++++++++++++++++++

::  

    yum install -y sudo device-mapper#必须安装
    yum install -y python-pip qemu-img kpartx
    yum install -y parted hdparm util-linux genisoimage
    yum install -y  squashfs-tools ##安装ubuntu镜像时需要使用



安装dib软件
++++++++++++++++++++++

.. note:: 这里我们不使用python virtual环境。直接用当前环境

::

    pip install diskimage-builder
    安装完成后，查看帮助文档
    [root@ttt yum.repos.d]# disk-image-create -h
    Usage: disk-image-create [OPTION]... [ELEMENT]...


准备镜像生成参数
++++++++++++++++++++++

首先我们创建一个目录用于生成镜像文件
-------------------------------------
::

    mkdir /data
    cd /data

定义镜像配置文件
-------------------------------------
::
    
    ##创建 vm_profile文件,用于定义环境变量,内容如下
    vim vm_profile

    export DIB_RELEASE=centos7   # 可替换为其他ubuntu系统代号名称
    export DIB_DISTRIBUTION_MIRROR=http://cn.archive.ubuntu.com/ubuntu  #可替换其他mirror
    export DIB_CLOUD_INIT_DATASOURCES="ConfigDrive, OpenStack, NoCloud"    #cloud-init datasource配置

    source vm_profile

    ==由于下载太慢，我们可以先将文件下载到本地==
    vim vm_profile
    export DIB_RELEASE=trusty
    #export DIB_CLOUD_IMAGES=172.28.12.35  ##http服务器跟路径
    export BASE_IMAGE_FILE=trusty-server-cloudimg-amd64-root.tar.gz ###文件名称
    #export DIB_DISTRIBUTION_MIRROR=https://mirrors.aliyun.com/ubuntu
    export DIB_CLOUD_INIT_DATASOURCES="ConfigDrive, OpenStack, NoCloud" 

执行制作
-------------------------------------
::

    disk-image-create ironic-agent centos7 -o ironic-agent

制作完成后，我们查看路径
-------------------------------------

git clone https://git.openstack.org/openstack/diskimage-builder
git clone https://github.com/openstack/trove-integration.git
git clone https://github.com/openstack/tripleo-image-elements