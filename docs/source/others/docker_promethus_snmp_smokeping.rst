.. _dpsm:


########################
prometheus 线路监控方案
########################



.. note :: 

   公司提出新的需求，需要监控总公司到各个子公司的线路质量的监控。能获取的资源包括
   出口的snmp信息以及互联ip地址，经过调研分析。
   这里采用promethus来监控采集数据。
   通过smokeping来采集互联地址的时延数据
   通过snmp协议来获取交换机端口数据

.. contents:: 目录

..
   section-numbering::


--------------------------


基本介绍
========================


Promethues
+++++++++++++
Prometheus 是一套开源的系统监控报警框架。它启发于 Google 的 borgmon 监控系统，
由工作在 SoundCloud 的 google 前员工在 2012 年创建，作为社区开源项目进行开发，
并于 2015 年正式发布。2016 年，Prometheus 正式加入 
Cloud Native Computing Foundation，成为受欢迎度仅次于 Kubernetes 的项目。

作为新一代的监控框架，Prometheus 具有以下特点：

* 强大的多维度数据模型：

    #. 时间序列数据通过 metric 名和键值对来区分。
    #. 所有的 metrics 都可以设置任意的多维标签。
    #. 数据模型更随意，不需要刻意设置为以点分隔的字符串。
    #. 可以对数据模型进行聚合，切割和切片操作。
    #. 支持双精度浮点类型，标签可以设为全 unicode。

* 灵活而强大的查询语句（PromQL）：在同一个查询语句，可以对多个 metrics 进行乘法、加法、连接、取分数位等操作。

* 易于管理： Prometheus server 是一个单独的二进制文件，可直接在本地工作，不依赖于分布式存储。
* 高效：平均每个采样点仅占 3.5 bytes，且一个 Prometheus server 可以处理数百万的 metrics。
* 使用 pull 模式采集时间序列数据，这样不仅有利于本机测试而且可以避免有问题的服务器推送坏的 metrics。
* 可以采用 push gateway 的方式把时间序列数据推送至 Prometheus server 端。
* 可以通过服务发现或者静态配置去获取监控的 targets。
* 有多种可视化图形界面。
* 易于伸缩。

需要指出的是，由于数据采集可能会有丢失，所以 Prometheus 
不适用对采集数据要 100% 准确的情形。但如果用于记录时间序列数据，
Prometheus 具有很大的查询优势，此外，Prometheus 适用于微服务的体系架构。

snmp
+++++++++++++

简单网络管理协议（SNMP） 是专门设计用于在 IP 网络管理网络节点（服务器、工作站、路由器、交换机及HUBS等）
的一种标准协议，它是一种应用层协议。

smokeping
+++++++++++++

Smokeping是rrdtool的作者TobiOetiker 的作品，是用Perl 写的，
主要是监视网络性能，包括常规的ping，
用echoping 监www 服务器性能，监视dns 查询性能，监视ssh 性能等

安装
========================


环境及版本说明
+++++++++++++++
* CentOS Linux release 7.6.1810 (Core)
* Docker version 18.09.6, build 481bc77156
* docker-compose version 1.18.0, build 8dd22a9


项目文件目录
+++++++++++++++
::

    ├── alertmanager
    │   └── config
    │       └── alertmanager.yml
    ├── alertmanager-dingtalk
    │   └── default.tmpl
    ├── clean.sh
    ├── docker-compose.yml
    ├── docker-compose.yml.bak
    ├── install.sh
    ├── prometheus
    │   ├── config
    │   │   ├── prometheus.yml
    │   │   └── rules.d
    │   │       └── alertmanager.rules
    │   └── target.json
    ├── README.md
    ├── smokeping
    │   ├── config
    │   │   ├── Alerts
    │   │   ├── Database
    │   │   ├── General
    │   │   ├── httpd.conf
    │   │   ├── location
    │   │   │   ├── szswzx
    │   │   │   └── szxf
    │   │   ├── pathnames
    │   │   ├── Presentation
    │   │   ├── Probes
    │   │   ├── site-confs
    │   │   │   └── smokeping.conf
    │   │   ├── Slaves
    │   │   ├── ssmtp.conf
    │   │   └── Targets
    │   └── data
    ├── smokeping-exporter
    │   ├── config
    │   │   └── smokeping_exporter.py
    │   └── Dockerfile
    ├── snmp-exporter
    │   └── config
    │       └── snmp.yml


docker-compose 文件
+++++++++++++++++++++++

    ::

        # Author: jack_lee (lifc@humenggroup.com)
        # Created: 2019/7/1
        # Desription: prms监控大屏部署启动

        version: '3'
        services:
        prometheus:
            image: prom/prometheus:v2.11.1
            restart: unless-stopped
            container_name: prms_prometheus
            networks:
            - backend
            depends_on:
            - alertmanager
            privileged: true
            links:
            - alertmanager
            - snmp-exporter
            - smokeping-exporter
            ports:
            - 19090:9090
            volumes:
            - /etc/localtime:/etc/localtime:ro
            - /data/prometheus/data:/prometheus
            - /data/prometheus/config:/etc/prometheus
            command: --web.enable-lifecycle
        alertmanager:
            image: prom/alertmanager:v0.18.0
            restart: unless-stopped
            container_name: prms_alertmanager
            networks:
            - backend
            depends_on:
            - alertmanager-dingtalk
            ports:
            - 19093:9093
            volumes:
            - /etc/localtime:/etc/localtime:ro
            - /data/alertmanager/data:/alertmanager
            - /data/alertmanager/config:/etc/alertmanager
        alertmanager-dingtalk:
            image: timonwong/prometheus-webhook-dingtalk
            restart: unless-stopped
            container_name: prms_alertmanager_dingtalk
            networks:
            - backend
            ports:
            - 18001:8001
            volumes:
            - /etc/localtime:/etc/localtime:ro
            - /data/alertmanager-dingtalk:/usr/share/prometheus-webhook-dingtalk/template
            command: --web.listen-address=":8001" --ding.profile="ops_dingtalk=https://oapi.dingtalk.com/robot/send?access_token=5561a13a71af02580c77c3a406a70bf1dca326ac28a87a4dbda435b7ebd365b2" --ding.timeout=10s  --log.level=debug
        smokeping:
            image: linuxserver/smokeping
            container_name: prms_smokeping
            networks:
            - backend
            environment:
            - PUID=1000
            - PGID=1000
            - TZ=Asia/Shanghai
            volumes:
            - /data/smokeping/config:/config
            - /data/smokeping/data:/data
            - /etc/localtime:/etc/localtime:ro
            ports:
            - 18002:8002
            restart: unless-stopped
        smokeping-exporter:
            image: smokeping-exporter
            container_name: prms_smokeping_exporter
            networks:
            - backend
            depends_on:
            - smokeping
            volumes:
            - /data/smokeping-exporter/config:/config
            - /data/smokeping/data:/data
            - /etc/localtime:/etc/localtime:ro
            ports:
            - 18003:8003
            command: -p 8003
            restart: unless-stopped
        snmp-exporter:
            image: prom/snmp-exporter:v0.15.0
            container_name: prms_snmp_exporter
            networks:
            - backend
            volumes:
            - /data/snmp-exporter/config:/etc/snmp_exporter
            - /etc/localtime:/etc/localtime:ro
            ports:
            - 19116:9116
            restart: unless-stopped
        networks:
        backend:


普罗米斯监控大屏部署文档
++++++++++++++++++++++++++++++

服务列表
--------

-  prms\_prometheus 普罗米修斯监控模块
-  prms\_alertmanager 普罗米修斯报警模块
-  prms\_alertmanager\_dingtalk 普罗米修斯钉钉报警插件
-  prms\_smokeping ping监控
-  smokeping-exporter smokeping 数据采集exporter
-  snmp-exporter 交换机snmp协议数据采集exporter

端口对应关系
-------------

+--------------------------------+------------+------------+----------------+
| 服务名称                       | 本地端口   | 外部端口   | 备注           |
+================================+============+============+================+
| prms\_prometheus               | 9090       | 19090      | 服务监听端口   |
+--------------------------------+------------+------------+----------------+
| prms\_alertmanager             | 9093       | 19093      | 服务监听端口   |
+--------------------------------+------------+------------+----------------+
| prms\_alertmanager\_dingtalk   | 8001       | 18001      | 服务监听端口   |
+--------------------------------+------------+------------+----------------+
| prms\_smokeping                | 8002       | 18002      | 服务监听端口   |
+--------------------------------+------------+------------+----------------+
| smokeping-exporter             | 8003       | 18003      | 服务监听端口   |
+--------------------------------+------------+------------+----------------+
| snmp-exporter                  | 9116       | 19116      | 服务监听端口   |
+--------------------------------+------------+------------+----------------+

安装部署
-------------

::

    chmod +x ./install.sh
    ./install.sh

清理环境
-------------


::

    chmod +x ./clean.sh
    ./clean.sh


---------------------

参考文档：

* http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
* https://kyzhang.me/2018/05/08/Sphinx-Readthedocs-GitHub2build-wiki/

