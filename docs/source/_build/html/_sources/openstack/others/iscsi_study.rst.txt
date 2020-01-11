
安装服务端
===========
::

    yum -y install scsi-target-utils

    #启动服务
    systemctl start tgtd
    systemctl enable tgtd

配置
=====

.. tip:: 

    指定CentOS7本机的sdb设备为iSCSI设备，注意sdb这个设备我只是挂上去，没有在系统上挂载和格式化，也千万不要格式化和挂载，然后用这个sdb创建iSCSI设备并授权192.168.100.0/24这个网段的可以访问

::

    tgtadm --lld iscsi --mode target --op new --targetname iqn.2019-04.cn.com.itox.iscsi:myscsi.disk1 --tid 1
    
    #指定磁盘
    tgtadm --lld iscsi --mode logicalunit --op new --tid 1 --lun 1 --backing-store /dev/sdb
    
    #指定访问网段
    tgtadm --lld iscsi --mode target --op bind --tid 1 --initiator-address 192.168.100.0/24
