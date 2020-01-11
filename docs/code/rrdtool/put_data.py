# -*- coding: utf-8 -*-
# !/usr/bin/python
import rrdtool
import time, psutil
import sys
import random

temp=0
total_output_traffic=0
total_input_traffic=int(sys.argv[6])
start=sys.argv[1]
end=sys.argv[2]
step=sys.argv[3]
randstart=sys.argv[4]
randend=sys.argv[5]
for starttime in range(int(start),int(end),int(step)):
    baseBw = random.randint(int(randstart),int(randend))
    temp = baseBw * 31457280
    total_input_traffic += temp
    update = rrdtool.updatev('/root/Flow2.rrd','%s:%s:%s' % (str(starttime), str(total_input_traffic), str(total_output_traffic)))

print total_input_traffic
