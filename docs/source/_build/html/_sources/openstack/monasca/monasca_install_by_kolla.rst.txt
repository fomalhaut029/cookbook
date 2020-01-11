.. _monasca_install_by_kolla:

###################
Monasca 安装(Kolla)
###################



.. contents:: 目录

..
   section-numbering::

--------------------------


编译镜像
========

.. note:: 由于我这边是通过源码编译的方式安装monasca，因此需要将monasca以及依赖的组件的镜像全部进行编译

::

    #进入kolla 虚拟环境
    source /opt/os_hum/kolla_env/bin/activate 

    #编译依赖组件
    python ./build.py monasca zookeeper elasticsearch 
    python ./build.py influxdb kibana grafana kafka logstash


开启monasca
===========

修改 ``/etc/kolla/globals.yml`` 文件，添加 ``enable_monasca: "yes"``

::

    ---
    kolla_base_distro: "centos"
    kolla_install_type: "source"
    kolla_dev_mode: true
    openstack_release: "8.0.1"
    kolla_internal_vip_address: "10.199.33.153"
    network_interface: "eth0"
    neutron_external_interface: "eth1"
    enable_haproxy: "no"
    enable_cinder: "yes"
    enable_cinder_backup: "no"
    enable_cinder_backend_nfs: "yes"
    enable_trove: "yes"
    cinder_backup_driver: "nfs"
    cinder_backup_share: "10.199.33.153:/opt/nfs/os/stein"
    nova_compute_virt_type: "qemu"
    #enable_ceilometer: "yes"
    #enable_panko: "yes"
    #enable_gnocchi: "yes"
    #enable_aodh: "yes"
    
    enable_monasca: "yes"


部署&安装
==========

::  
    
    #进入虚拟环境
    source /opt/os_hum/kolla-ansible_env/bin/activate

    #安装部署
    cd /opt/os_hum/kolla-ansible/tools/

    ./kolla-ansible bootstrap-servers
    ./kolla-ansible  prechecks
    ./kolla-ansible  deploy
    ./kolla-ansible  post-deploy

    #生成环境变量
    source /etc/kolla/admin-openrc.sh


配置libvirt插件
===============

::

  

    #进入monasca collector容器 安装libvirt插件
    docker exec -it -u 0 monasca_agent_collector bash

    # 安装libvirt系统组件
    yum install -y libvirt libvirt-devel

    #进入容器python虚拟环境
    source /var/lib/kolla/venv/bin/activate

    

    #安装monasca libvirt插件 执行此命令将会安装libvirt-python
    pip install monasca-agent[libvirt]




