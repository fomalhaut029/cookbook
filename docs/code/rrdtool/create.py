# -*- coding: utf-8 -*-
#!/usr/bin/python
import rrdtool
import time
 
 start=sys.argv[1]
# 获取当前Linux时间戳作为rrd起始时间
cur_time=str(int(start))
# 数据写频率--step为300秒（即5分钟一个数据点）
rrd=rrdtool.create('Flow.rrd','--step','300','--start',cur_time,
# 定义数据源enp0s3_in（入流量）、enp0s3_out（出流量）；类型都为COUNTER（递增）
# 600秒为心跳值，其含义是600秒没有收到值，则会用UNKNOWN代替；
# 0为最小值；最大值用U代替，表示不确定
    'DS:enp0s3_in:COUNTER:600:0:U',
    'DS:enp0s3_out:COUNTER:600:0:U',
# RRA定义格式为[RRA：CF：xff：steps：rows]
# CF定义了AVERAGE、MAX、MIN三种数据合并方式
# xff定义为0.5，表示一个CDP中的PDP值如超过一半值为UNKNOWN，则该CDP的值就被标为 UNKNOWN
# 下列前4个RRA的定义说明如下，其他定义与AVERAGE方式相似，区别是存最大值与最小值
# 每隔5分钟（1*300秒）存一次数据的平均值，存600笔，能存2.08天数据
# 每隔30分钟（6*300秒）存一次数据的平均值，存700笔，能存14.58天（2周）数据
# 每隔2小时（24*300秒）存一次数据的平均值，存775笔，能存64.58天（2个月）数据
# 每隔24小时（288*300秒）存一次数据的平均值，存797笔，能存797天（2年）数据
    'RRA:AVERAGE:0.5:1:600',
   'RRA:AVERAGE:0.5:6:700',
   'RRA:AVERAGE:0.5:24:775',
   'RRA:AVERAGE:0.5:288:797',
   'RRA:MAX:0.5:1:600',
   'RRA:MAX:0.5:6:700',
   'RRA:MAX:0.5:24:775',
   'RRA:MAX:0.5:444:797',
   'RRA:MIN:0.5:1:600',
   'RRA:MIN:0.5:6:700',
   'RRA:MIN:0.5:24:775',
   'RRA:MIN:0.5:444:797')
if rrd:
    print rrdtool.error()