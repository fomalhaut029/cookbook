#!/bin/bash
rm -f /root/Flow.rrd
rm -f /root/Flow.png
python /root/create.py 1574726400
temp=`python /root/put_data.py 1574726700 1574730000 300 2 5 0`
temp=`python /root/put_data.py 1574730300 1574731800 300 15 25 "$temp"`
temp=`python /root/put_data.py 1574732100 1574740800 300 35 55 "$temp"`
temp=`python /root/put_data.py 1574741100 1574743200 300 10 15 "$temp"`
temp=`python /root/put_data.py 1574743500 1574748000 300 2 5 "$temp"`
temp=`python /root/put_data.py 1574748300 1574762400  300 35 55 "$temp"`
temp=`python /root/put_data.py 1574762700 1574764800  300 10 15 "$temp"`
temp=`python /root/put_data.py 1574765100 1574768400 300 2 5 "$temp"`
python /root/graph.py -25h -15h "J23-2950 - Traffic - Fa0/18 -  183.63.53.38|106.3.228.38 50M独享"
