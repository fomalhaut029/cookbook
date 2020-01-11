.. _switch-cmd-list:

################
常用交换机命令
################

.. note :: 

    记录常用的交换机命令：


场景1： 配置端口2/0/4 access vlan 32
=====================================

#. 查看端口情况

::

    L15_C3750-Stack#sh run in gi 2/0/4 #查看端口情况

    Building configuration...

    Current configuration : 181 bytes
    !
    interface GigabitEthernet2/0/4
    description TO L15_ROS ETH1
    switchport trunk encapsulation dot1q
    switchport trunk allowed vlan 2,32-34,118
    switchport mode trunk
    shutdown
    end

#. 清理原来的配置信息并配置
::

    L15_C3750-Stack#configure terminal   #进入配置模式
    L15_C3750-Stack(config)#default interface gigabitEthernet  2/0/4  #将端口设置为默认模式
    L15_C3750-Stack(config)#int gigabitEthernet  2/0/4 #配置端口2/0/4
    L15_C3750-Stack(config-if)#sw mode access #设置端口模式
    L15_C3750-Stack(config-if)#sw access vlan 32 #设置端口为access vlan 32 


场景1： 配置端口2/0/14 trunk vlan 100-150
============================================

:: 

    L15_C3750-Stack#configure terminal   #进入配置模式
    L15_C3750-Stack(config)#default interface gigabitEthernet  2/0/4  #将端口设置为默认模式
    L15_C3750-Stack(config)#int gigabitEthernet  2/0/4 #配置端口2/0/4
    L15_C3750-Stack(config-if)#switchport trunk encapsulation dot1q #设置端口模式
    L15_C3750-Stack(config-if)#switchport mode trunk 
    L15_C3750-Stack(config-if)#sw trunk allowed vlan 32 #设置端口为access vlan 32 

    L15_C3750-Stack(config-if)#sw trunk allowed vlan add 100-150 #添加vlan


删除默认的全部放行vlan
=========================
::
    
    switchport trunk allowed vlan remove 1-4094


查看交换机信息
===============

::
    show version
