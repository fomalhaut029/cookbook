# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Date: 2017/4/5
# Created by 独自等待
from netmiko import ConnectHandler
import time
import os
import json
from flask import Flask
app = Flask(__name__)


def Cisco(dev,exec_cmd):
    print('正在连接交换机：%s\n' % (dev))
    if dev['type'] == 'cisco':
        "思科交换机配置导出函数"
        cisco = {
            'device_type': 'cisco_ios_telnet',
            'ip': dev['ip'],
            'username': 'autobackup',
            'password': 'Backup@admin',
            'port': 23,  # optional, defaults to 22
            'secret': '',  # optional, defaults to ''
            'verbose': False,  # optional, defaults to False
        }
        net_connect = ConnectHandler(**cisco)
        net_connect.enable()
        
        print('正在执行cisco命令：' + exec_cmd)
        net_connect.send_command('wr')
        net_connect.send_command_timing(exec_cmd)
        net_connect.send_command_timing("\n")
        net_connect.send_command_timing("\n")
    elif dev['type'] == 'huawei':
        "华为交换机配置导出函数"
        huawei = {
            'device_type': 'huawei_telnet',
            'ip': dev['ip'],
            'username': 'autobackup',
            'password': 'Backup@admin',
            'port': 23,  # optional, defaults to 22
            'secret': '',  # optional, defaults to ''
            'verbose': False,  # optional, defaults to False
        }
        net_connect = ConnectHandler(**huawei)
        net_connect.enable()

        print('正在执行huawei命令：' + exec_cmd)
        net_connect.send_command('save')
        net_connect.send_command_timing(exec_cmd)


    print('命令执行完毕，结果保存于tftp服务中!\n')
    net_connect.disconnect()


if __name__ == '__main__':

    base_command = 'copy startup-config tftp://172.28.12.35'
    timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    with open(r'docs\code\dev.json','rb') as f:
        dev_list = json.loads(f.read())
        for dev in dev_list:
            exec_cmd = "%s/%s/%s/%s/%s-%s-config" %(base_command,dev['zone'],dev['pod'],dev['cluster'],dev['name'],timestr)
            Cisco(dev,exec_cmd)