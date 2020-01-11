.. _monasca:

#############
Monasca 介绍
#############


.. contents:: 目录

..
   section-numbering::

--------------------------

架构图
======

.. figure:: /_static/images/monasca_architecture.png
   :scale: 100
   :align: center

组件介绍
========

主要组件:

- monasca-api: Monasca REST API
- monasca-persister: 接收、处理监控告警数据，并写入到时序数据库
- monasca-thresh: 阈值引擎，处理度量并确定报警状态，发布告警信息
- monasca-notification: 接收告警信息当报警状态转换时通知用户
- monasca-agent: 从节点、服务、应用程序、普罗米修斯端点收集度量值，数据采集器
- monasca-log-api: 用于在Monasca中处理日志数据的API
- monasca-aggregator: 实时数据聚合引擎

主要部署方式
============

- monasca-docker: Docker containers and the docker-compose 
  development environment
- monasca-helm: Helm charts for deployment in Kubernetes
- puppet-monasca: puppet modules for deploying Monasca in 
  OpenStack
- os_monasca, os_monasca-agent, os_monasca-ui: Ansible modules for 
  deployment in an OpenStack environment
- rpm-packaging: RPM spec file templates and tooling for building 
  OpenStack packages for RPM based distributions
- Devstack may also be a valuable reference for development and as an 
  example of how to configure the set of Monasca services.

客户端软件包
============

- python-monascaclient: CLI and Python library 
  for interating with the Monasca API
- monasca-statsd: statsd-compatible library for sending metrics from 
  instrumented applications to Monasca

集成
====
- grafana: Forked version of Grafana that adds support 
  for Keystone authentication
- monasca-grafana-datasource: Monasca data source for Grafana
- monasca-grafana-app: Application plugin for Grafana
- monasca-ui: Monasca UI for OpenStack Horizon
- monasca-kibana-plugin: Keystone authentication support 
  and multi-tenancy for Kibana 4.6.x
- monasca-transform: Transformation and aggregation of data in Monasca
- monasca-ceilometer: Plugin and storage driver for Ceilometer to 
  send samples to Monasca, also known as Ceilosca
