#!/bin/bash
# 
# 单机安装ceph rbd&rgw环境,结合openstack
# 


#设置主机名称
echo "nameserver 114.114.114.114" > /etc/resolv.conf
IP=`ip route get 114.114.114.114 | awk 'NR==1 {print $NF}'`
hostnamectl set-hostname ceph-01
HOSTNAME=ceph-01
echo $IP $HOSTNAME >>  /etc/hosts


yum clean all
rm -rf /etc/yum.repos.d/*.repo
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
sed -i '/aliyuncs/d' /etc/yum.repos.d/CentOS-Base.repo
sed -i 's/$releasever/7/g' /etc/yum.repos.d/CentOS-Base.repo
sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo
yum makecache

sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
setenforce 0
systemctl stop firewalld 
systemctl disable firewalld

echo "
[ceph]
name=ceph
baseurl=https://mirrors.aliyun.com/ceph/rpm-nautilus/el7/x86_64/
gpgcheck=0
[ceph-noarch]
name=cephnoarch
baseurl=https://mirrors.aliyun.com/ceph/rpm-nautilus/el7/noarch/
gpgcheck=0
[ceph-source]
name=Ceph source packages
baseurl=https://mirrors.aliyun.com/ceph/rpm-nautilus/el7/SRPMS
gpgcheck=0
" > /etc/yum.repos.d/ceph.repo

yum install ceph ceph-radosgw ceph-deploy -y



ceph-deploy new $HOSTNAME

PUBLIC_NETWORK=${IP:}
echo osd_pool_default_size = 1 >> ceph.conf
echo public_network = ${IP%.*}.0/24 >> ceph.conf
echo mon_max_pg_per_osd = 300 >> ceph.conf
echo osd_pool_default_size = 1 >> ceph.conf
echo osd_pool_default_min_size = 1 >> ceph.conf

ceph-deploy install --release nautilus $HOSTNAME

ceph-deploy mon create-initial
ceph-deploy admin $HOSTNAME
ceph-deploy mgr create $HOSTNAME
ceph-deploy osd create --bluestore $HOSTNAME --data /dev/sdb

ceph-deploy install --rgw $HOSTNAME
ceph-deploy rgw create $HOSTNAME




echo "
[client.rgw.$HOSTNAME]
rgw_frontends = \"civetweb port=80\"
" >>/etc/ceph/ceph.conf

sudo systemctl restart ceph-radosgw@rgw.$HOSTNAME
ceph -s

echo install ceph done

ceph osd pool create images 64 64
ceph osd pool create volumes 64 64
ceph osd pool create backups 64 64
ceph osd pool create vms 64 64
ceph osd pool create gnocchi 64 64
ceph osd pool application enable images rbd
ceph osd pool application enable volumes rbd
ceph osd pool application enable backups rbd
ceph osd pool application enable vms rbd
ceph osd pool application enable gnocchi rbd

rados lspools |grep -v "rgw"

echo create glance user
ceph auth get-or-create client.glance
ceph auth caps client.glance mon 'allow r' osd 'allow class-read object_prefix rbd_children,allow rwx pool=images'
ceph auth get client.glance -o /etc/ceph/ceph.client.glance.keyring

echo create cinder user
ceph auth get-or-create client.cinder
ceph auth caps client.cinder mon 'allow r' osd 'allow class-read object_prefix rbd_children,allow rwx pool=volumes,allow rwx pool=backups'
ceph auth get client.cinder -o /etc/ceph/ceph.client.cinder.keyring

echo create nova user
ceph auth get-or-create client.nova
ceph auth caps client.nova mon 'allow r' osd 'allow class-read object_prefix rbd_children,allow rwx pool=vms'
ceph auth get client.nova -o /etc/ceph/ceph.client.nova.keyring

echo create gnocchi user
ceph auth get-or-create client.gnocchi
ceph auth caps client.gnocchi mon 'allow r' osd 'allow class-read object_prefix rbd_children,allow rwx pool=gnocchi'
ceph auth get client.gnocchi -o /etc/ceph/ceph.client.gnocchi.keyring


ceph auth list
