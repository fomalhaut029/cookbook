#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import os
import json

def register_baremetal_node(baremetal_info):
    print("注册裸机节点：{0}".format(baremetal_info))

    
    print()

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path+'/node.json','rb') as f:
        baremetal_list = json.loads(f.read())
        for baremetal_info in baremetal_list:
            print(" ".join(baremetal_info.values()))
            cmd = "/bin/sh {0} {1}".format(path+"/init-baremetal.sh"," ".join(baremetal_info.values()))
            os.system(cmd)