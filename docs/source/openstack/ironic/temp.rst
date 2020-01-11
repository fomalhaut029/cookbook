.. temp:

#################################
Ironic 临时笔记
#################################

Ironic 映像
=============

ironic有两种类型的镜像 **deploy镜像** , **user 镜像** 

.. note:: 
    ironic 整个部署流程中有两组映像，分别是 deploy 映像和 user 映像， 其中 deploy 映像用在 inspector 和 部署阶段， user 映像是用户需要安装的操作系统映像。
    制作ironic deploy镜像其实就是在普通镜像中添加一个ipa服务，用来裸机和ironic通信。 官方推荐制作镜像的工具有两个，分别是CoreOS tools和disk-image-builder


deploy 镜像
++++++++++++++++++++
.. note:: 获取deploy镜像有两种方式：1、通过官方下载制作好的镜像, 2、通过dib工具制作。有时候
    部署裸机的时间比较长。我们需要登入到部署系统中查看情况,两种方式制作的镜像都需要设置登入的方式


官网下载镜像
--------------
Ironic的deploy镜像可以直接通过官网下载, 下载链接：http://tarballs.openstack.org/ironic-python-agent/coreos/files/
分别下载两个文件：

* `coreos_production_pxe-master.vmlinuz <http://tarballs.openstack.org/ironic-python-agent/coreos/files/coreos_production_pxe-master.vmlinuz>`_
* `coreos_production_pxe_image-oem-master.cpio.gz <http://tarballs.openstack.org/ironic-python-agent/coreos/files/coreos_production_pxe_image-oem-master.cpio.gz>`_

将镜像上传到glance中
::

    openstack image create --disk-format aki --container-format aki --public \
    --file coreos_production_pxe-master.vmlinuz deploy-vmlinuz

    openstack image create --disk-format ari --container-format ari --public \
    --file coreos_production_pxe_image-oem-master.cpio.gz deploy-initrd

设置镜像登入密码
^^^^^^^^^^^^^^^^^^^
官方的coreos镜像没有设置默认的密码,我们可以通过设置 在 ``pxe_append_params`` 中 
设置 ``coreos.autologin`` 跳过登入

::

    # cat /etc/ironic/ironic.conf 
    [pxe]
    pxe_append_params = nofb nomodeset vga=normal coreos.autologin ipa-debug=1"


另外为了便于调试，可以打开IPA的DEDUG功能，在 ``pxe_append_params`` 追加 ``ipa-debug=1``


通过dib制作镜像
-----------------
dib制作的镜像可以设置密码或者ssh key登入deploy系统.
dib 是通过 ``dynamic-login`` 这个元素来实现密码登入的,下面是 ``dynamic-login`` 的执行脚本:
::

    set -eu
    set -o pipefail

    # Reads an encrypted root password from the kernel command line and set
    # it to the root user
    if [[ $(</proc/cmdline) =~ rootpwd=\"([^\"]+)\" ]]; then
        echo "root:${BASH_REMATCH[1]}" | chpasswd -e
    fi

    # Reads a sshkey from the kernel command line and appends it to the root
    # user authorized_keys
    SSHDIR=/root/.ssh
    if [[ $(</proc/cmdline) =~ sshkey=\"([^\"]+)\" ]]; then
        mkdir -p $SSHDIR
        chmod 700 $SSHDIR
        echo "${BASH_REMATCH[1]}" > $SSHDIR/authorized_keys
        chmod 600 $SSHDIR/authorized_keys
    fi

我们首先制作带 ```dynamic-login`` 的部署镜像
::

    disk-image-create deploy-baremetal centos7 dynamic-login -o ironic-agent

关于dib的基本使用可以参照  :ref:`openstack-dib_make_ironic-agent` 

制作完镜像后。我们需要配置 ``/etc/kolla/config/ironic.conf`` ,我们这里使用的是kolla部署的，因此调整完这个文件后
需要kolla-ansbile reconfigure ,如果要及时生效，也可以修改/etc/kolla/ironic/ironic.conf 文件。然后重启docker容器


* ssh方式 ：
  注入ssh key，修改ironic配置文件，pxe_append_params追加sshkey="ssh-rsa AAAA..."

::
    
    # cat ~/.ssh/id_rsa.pub 
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC60V3ZKk0+c3LcR3TtDbLCtnlPn7fLWmkS/KS0lQ/V5wKOXrtgZPNDCkkOwCzwC0A6HXIfllTKsaaf5HMJw8siwL6Qnmu6GpUR597QVIZ7DW1eoYBqz2MFg8lxRk9BjZ3J3IHUbqFoaVHW+k6K+d3pEXi0knR+RoIWqPKY02ImT2ThN/RZtUh4iiy6fMgzlWhsyqkOKr8uoYjLF1AC6frqLSXzAJbqGriyI4VnqqKhUtcDZFeRWHkgZ7DRVXMo1TOMpm82k56Dac3iXW++pE4r+Us603VvWf2B28FowQjxNRlNWIIsXe7RMCN6EFxypmu8113cVP23+n1Jkis3Ro37 root@zx-120

将sshkey 写入到配置文件中：
::

    [pxe]
    pxe_append_params = sshkey="AAAAB3NzaC1yc2EAAAADAQABAAABAQC60V3ZKk0+c3LcR3TtDbLCtnlPn7fLWmkS/KS0lQ/V5wKOXrtgZPNDCkkOwCzwC0A6HXIfllTKsaaf5HMJw8siwL6Qnmu6GpUR597QVIZ7DW1eoYBqz2MFg8lxRk9BjZ3J3IHUbqFoaVHW+k6K+d3pEXi0knR+RoIWqPKY02ImT2ThN/RZtUh4iiy6fMgzlWhsyqkOKr8uoYjLF1AC6frqLSXzAJbqGriyI4VnqqKhUtcDZFeRWHkgZ7DRVXMo1TOMpm82k56Dac3iXW++pE4r+Us603VvWf2B28FowQjxNRlNWIIsXe7RMCN6EFxypmu8113cVP23+n1Jkis3Ro37"

* password方式 :
  通过在 ``pxe_append_params`` 中添加 ``rootpwd`` 实现,从 ``dynamic-login`` 
  脚本中可以看出, ``rootpwd`` 
  设置的是一个密文的密码。因此我们需要通过openssl获取密码的密文

::

    (dib_env) [root@openstack-dib opt]# openssl 
    OpenSSL> passwd
    Password: 
    Verifying - Password: 
    9NF5pDgCPP2wY
    OpenSSL> 

将生成的密码密文 9NF5pDgCPP2wY 设置的配置文件中
::

    # cat /etc/ironic/ironic.conf

    [pxe]
    pxe_append_params = rootpwd="9NF5pDgCPP2wY"


整合上述情况后可以设置为如下配置：
::

    # cat /etc/ironic/ironic.conf 
    [pxe]
    pxe_append_params = nofb nomodeset rootpwd="9NF5pDgCPP2wY" vga=normal coreos.autologin ipa-debug=1 sshkey="ssh-dss AAAA..."


用户镜像
+++++++++++



其他
========
#. 切换用户

::
    
    alias openmember='openstack --os-project-name project-152202708661111 --os-username 152202708661111 --os-password password'

#. aa


参考引用
=========

.. [#] https://int32bit.me/2019/04/23/OpenStack-Ironic%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%E5%8F%82%E8%80%83/#
