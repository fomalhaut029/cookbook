# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 0004 17:01
# @Author  : dyl
# @File    : demo.py
# @Software: PyCharm
from flask import Flask
from flask import request
import time
import json
import requests

from switch_config_bakcup import Cisco
app = Flask(__name__)


@app.route('/save', methods=['POST'])
def save_config():

    tftp_host = '10.255.88.4'
    cisco_base_command = 'copy startup-config tftp://%s' % tftp_host
    huawei_base_command = 'tftp %s put vrpcfg.zip' % tftp_host
    timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    data = request.get_data()
    user_info = json.loads(json.loads(data).get('user_info'))
    dev_list = json.loads(json.loads(data).get('dev_list'))
    # 备份成功后，回调接口
    url = 'http://172.28.12.32:7788/backup/callBack'
    for dev in dev_list:

        try:
            dev_id = dev.pop('id') # 设备ID,用于回调
            if dev['type'] == 'cisco':
                exec_cmd = '%s/%s/%s/%s/%s-%s-config' % (cisco_base_command, dev['zone'], dev['pod'], dev['cluster'], dev['name'], timestr)
            else:
                exec_cmd = '%s /%s/%s/%s/%s-%s-config' % (huawei_base_command, dev['zone'], dev['pod'], dev['cluster'], dev['name'], timestr)
            print(exec_cmd)
           # Cisco(dev, exec_cmd)
            path = '/%s/%s/%s/%s-%s-config' % (dev['zone'], dev['pod'], dev['cluster'], dev['name'], timestr)
            user_info.update({'content': '设备:' + dev['name'] + '备份成功', 'path': path, 'dev_id': dev_id, 'tftp_host': tftp_host})
            requests.post(url, data=user_info)
        except Exception as e:
            print('send cmd is error: %s' % e.__str__())
            user_info.update({'content': '设备:' + dev['name'] + '备份失败' + e.__str__()})
            requests.post(url, data=user_info)
    return "success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
