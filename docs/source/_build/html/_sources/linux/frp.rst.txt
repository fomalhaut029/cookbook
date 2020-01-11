
.. _frp:

##########################################
内网穿透-FRP
##########################################

frp 是一个高性能的反向代理应用，可以帮助您轻松地进行内网穿透，对外网提供服务，支持 tcp, udp, http, https 等协议类型，
并且 web 服务支持根据域名进行路由转发。

.. note:: 项目地址：
     码云: https://gitee.com/yijicai/frp/  github: https://github.com/fatedier/frp/


使用场景
=========
#. 内网穿透-类似花生壳，对于没有公网ip的内网用户,可以利用内网机子。提供外网http\https服务
#. 对于 http 服务支持基于域名的虚拟主机，支持自定义域名绑定，使多个域名可以共用一个80端口
#. 用处于内网或防火墙后的机器，对外网环境提供 tcp 服务，例如在家里通过 ssh 访问处于公司内网环境内的主机。

安装部署
========

.. note:: 软件下载地址：https://github.com/fatedier/frp/releases\
     
我们这里以linux为例：
下载解压
++++++++
::

     mkdir -p /usr/local/frp/
     wget -O /usr/local/frp/frp.tar.gz https://github.com/fatedier/frp/releases/download/v0.29.1/frp_0.29.1_linux_amd64.tar.gz 
     cd  /usr/local/frp/
     tar xzvf frp.tar.gz
     mv frp_0.29.1_linux_amd64 frp


将frp注册为服务
++++++++++++++++
::
     
     #注册服务端服务
     mkdir /etc/frp
     cp frps.ini /etc/frp/frps.ini
     tee /usr/lib/systemd/system/frps.service <<EOF
     [Unit]
     Description=frps
     After=network.target
     
     [Service]
     TimeoutStartSec=30
     ExecStart=/usr/local/frp/frp/frps -c /etc/frp/frps.ini
     ExecStop=/bin/kill $MAINPID
     
     [Install]
     WantedBy=multi-user.target
     EOF

     #注册客户端服务（我这里服务端和客户端位于同一个服务）
     cp frpc.ini /etc/frp/frpc.ini
     tee /usr/lib/systemd/system/frpc.service <<EOF
     [Unit]
     Description=frpc
     After=network.target
     
     [Service]
     TimeoutStartSec=30
     ExecStart=/usr/local/frp/frp/frpc -c /etc/frp/frpc.ini
     ExecStop=/bin/kill $MAINPID
     
     [Install]
     WantedBy=multi-user.target
     EOF


     #启动服务
     systemctl enable frps
     systemctl start frps
     systemctl status frps

     systemctl enable frpc
     systemctl start frpc
     systemctl status frpc


使用场景
+++++++++++++
- ssh访问内网服务器

::

     vi /etc/frp/frpc.ini
     #加入以下内容
     [ssh-10.199.32.123]
     type = tcp #转发协议
     local_ip = 10.199.32.123 #内网服务器ip
     local_port = 22 #内网服务器ssh端口
     remote_port = 12322 #代理服务器（frps服务器端口）

     连接：我的frps地址为：172.28.12.252
     ssh 172.28.12.252 12322

- sfa



