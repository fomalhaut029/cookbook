.. others:

#################################
Ironic 相关概览及以及延伸知识
#################################

由于Openstack Baremetal组件涉及的知识内容很多，本文将相关的知识点整理记录下来，方便
以后查阅


.. contents:: 目录

..
   section-numbering::

--------------------------


硬件管理驱动
=============
::

   enabled_hardware_types = ipmi,redfish

目前Ironic支持的类型包括 (在 ``https://opendev.org/openstack/ironic/src/branch/master/setup.cfg``)：
::

   fake-hardware = ironic.drivers.fake_hardware:FakeHardware
   ibmc = ironic.drivers.ibmc:IBMCHardware
   idrac = ironic.drivers.drac:IDRACHardware
   ilo = ironic.drivers.ilo:IloHardware
   ilo5 = ironic.drivers.ilo:Ilo5Hardware
   intel-ipmi = ironic.drivers.intel_ipmi:IntelIPMIHardware
   ipmi = ironic.drivers.ipmi:IPMIHardware
   irmc = ironic.drivers.irmc:IRMCHardware
   manual-management = ironic.drivers.generic:ManualManagementHardware
   redfish = ironic.drivers.redfish:RedfishHardware
   snmp = ironic.drivers.snmp:SNMPHardware
   xclarity = ironic.drivers.xclarity:XClarityHardware

.. tip:: ipmi 和 redfish都是通用的 远程控制管理驱动，ilo irmc等都是特定供应商的管理程序


这里对主要使用的类型做一个简单的介绍：

* ipmi ：IPMI (Intelligent Platform Management Interface)是一个开放的标准硬件管理接口规范。
  BMC (Baseboard Management Controller 基板管理控制器)是一个IPMI具体的实现

* redfish ：简单来说下一代IPMI.

* ilo ilo5 : 用于惠普服务器的远程控制驱动


硬件接口
==========




引导程序
==========

* bios : BIOS即Basic Input/Output System，翻成中文是“基本输入/输出系统”，
   是一种所谓的“固件”，负责在开机时做硬件启动和检测等工作，并且担任操作系统控制硬件时的中介角色
* uefi : 新型UEFI，全称“统一的可扩展固件接口”(Unified Extensible Firmware Interface)， 
   是一种详细描述类型接口的标准。这种接口用于操作系统自动从预启动的操作环境，加载到一种操作系统上








