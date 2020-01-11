.. _ironic_install_with_packstack:

#################################
通过packstack 安装Ironic 安装
#################################

本文介绍通过packstack来安装Ironic环境


.. contents:: 目录

..
   section-numbering::

--------------------------


环境说明
========
* CentOS Linux release 7.6.1810 (Core)
* openstack stein


环境准备
========

关闭防火墙
++++++++++++++++++++++
::

   systemctl stop firewalld
   systemctl disable firewalld 

关闭selinx ``/etc/selinux/config``
+++++++++++++++++++++++++++++++++++++++++++
::

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

   setenforce 0

安装packstack
==============
.. note:: 具体参照：https://wiki.openstack.org/wiki/Packstack

::

   #添加packstack源
   yum -y install centos-release-openstack-stein
   
   # 安装openstack-packstack
   yum -y install openstack-packstack

   # 生成answer-file
   packstack --gen-answer-file=packstack.cfg

配置packstack安装文件 ``packstack.cfg``
========================================

启用ironic，并修改ML2驱动为openvswitch

.. warning:: packstack默认配置的是ovn ，我当前环境中使用ovn安装一直失败。因此更改为openvswitch

::

   CONFIG_NEUTRON_ML2_MECHANISM_DRIVERS=openvswitch
   CONFIG_NEUTRON_L2_AGENT=openvswitch
   CONFIG_IRONIC_INSTALL=y




安装openstack
==============
::

   #启用debug模式。方便排查安装过程中的错误信息
   packstack --answer-file=packstack.cfg --debug
   #安装完成后，设置环境变量
   source keystonerc_admin


配置ironic
=============

.. note:: 通过packstack安装后，会自动配置ironic环境，我们这里了解一下配置信息。便于理解

keystone配置
++++++++++++++++++++++
::

   # 注册ironic服务用户openstack user create
   [root@packstack ~(keystone_admin)]# openstack user show ironic
   +---------------------+----------------------------------+
   | Field               | Value                            |
   +---------------------+----------------------------------+
   | domain_id           | default                          |
   | email               | ironic@localhost                 |
   | enabled             | True                             |
   | id                  | b4b9e5e191c549cea8ae8e85df56ad0b |
   | name                | ironic                           |
   | options             | {}                               |
   | password_expires_at | None                             |
   +---------------------+----------------------------------+

   #注册服务
   [root@packstack ~(keystone_admin)]# openstack service show ironic
   +-------------+----------------------------------------+
   | Field       | Value                                  |
   +-------------+----------------------------------------+
   | description | Ironic Bare Metal Provisioning Service |
   | enabled     | True                                   |
   | id          | 95d5b2d4321443139906a5b03ce64346       |
   | name        | ironic                                 |
   | type        | baremetal                              |
   +-------------+----------------------------------------+

   #创建endpoint,会创建三个类型[ admin public internal ]的endpoint
   [root@packstack ~(keystone_admin)]# openstack endpoint list --service ironic
   +----------------------------------+-----------+--------------+--------------+---------+-----------+---------------------------+
   | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                       |
   +----------------------------------+-----------+--------------+--------------+---------+-----------+---------------------------+
   | 9a55a7197d0e4484a78de938ec1cab55 | RegionOne | ironic       | baremetal    | True    | public    | http://10.199.32.112:6385 |
   | f1e242065a834f1a906f93e852dd0b72 | RegionOne | ironic       | baremetal    | True    | admin     | http://10.199.32.112:6385 |
   | f5e8a04432004863b3f55f30aca42a76 | RegionOne | ironic       | baremetal    | True    | internal  | http://10.199.32.112:6385 |
   +----------------------------------+-----------+--------------+--------------+---------+-----------+---------------------------+


nova配置
++++++++++++++++++++++
::
   
   # nova配置文件
   compute_driver=ironic.IronicDriver

   #
















遇到的问题
=====================
1. 

::

   Error: Systemd start for neutron-server failed!
   journalctl log for neutron-server:
   -- Logs begin at Sun 2019-09-29 11:51:18 CST, end at Sun 2019-09-29 13:48:13 CST. --
   Sep 29 13:43:15 packstack neutron-server[31338]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprecated.  Call .resolve and .require separately.
   Sep 29 13:43:15 packstack neutron-server[31338]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
   Sep 29 13:43:16 packstack neutron-server[31338]: The following mechanism drivers were not found: set(['ovnopenvswitch'])
   Sep 29 13:43:16 packstack systemd[1]: neutron-server.service: main process exited, code=exited, status=1/FAILURE

通过编辑：``/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py`` 解决
::

   删除掉：return pkg_resources.EntryPoint.parse("x="+s).load(False)
   添加：
   ep = pkg_resources.EntryPoint.parse("x=" + s)
   if hasattr(ep, 'resolve'):
      # this is available on setuptools >= 10.2
      return ep.resolve()
   else:
      # this causes a DeprecationWarning on setuptools >= 11.3
      return ep.load(False) 


2. 

::

   ERROR : Error appeared during Puppet run: 10.199.32.115_controller.pp
   Error: unable to connect to node rabbit@ironic2: nodedown
   You will find full trace in log /var/tmp/packstack/20191010-124333-hi4Rix/manifests/10.199.32.115_controller.pp.log

直接把服务全部关闭
::

   # 先把rabbitmq进程杀掉
   $ ps -ef | grep rabbitmq | grep -v grep | awk '{print $2}' | xargs kill -9







