#!/usr/bin/python3
# -*- coding:utf-8 -*-
import paramiko
import time

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)


def execute(addr):

    ssh.connect(addr, 23, 'lifc', '88878978', timeout=200)
    ssh_shell = ssh.invoke_shell()

    for script in scripts:
        ssh_shell.send(script)
        time.sleep(0.1)


if __name__ == '__main__':

    # 要批量执行脚本的设备
    devices = ['10.199.35.253']

    # 要批量执行的脚本
    scripts = ['display acl all\n']

    for device in devices:
        execute(device)