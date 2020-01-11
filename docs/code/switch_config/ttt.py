import time
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import sys
import getpass
from datetime import datetime
import os

def NetworkDevice(username,password,iplist,enablepass):
    rt = {
        'device_type':'cisco_ios',
        'username':username,
        'password':password,
        'ip': iplist,
        'secret':enablepass
    }

    print('-' * 50)
    print(u'[+] connecting to network device {0}...'.format(iplist))
    net_connect = ConnectHandler(**rt)
    net_connect.enable()

    hostname = net_connect.find_prompt().replace("#", "")
    print (u'[+] hostname:{0}'.format(hostname))

    timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    cmd = 'show running'
    filename = (u'{0}_{1}_{2}.txt'.format(iplist,cmd,timestr))
    filepath = r'C:\netpy\5pyresult\/'
    if os.path.exists(filepath):
        message = 'OK,the  "%s" dir exists.'
    else:
        message =  "Now, I will create the %s"
        os.makedirs(filepath)
    save = open(filepath + filename,'w')
    print(u'[+] executing {0} command'.format(cmd))
    output = net_connect.send_command(cmd)
    time.sleep(2)
    save.write(output)
    print(u'[+] {0} command executed,result was saved at {1}!'.format(cmd,filename))
    save.close()
    net_connect.disconnect()

if __name__ == '__main__':
    print ("[+] The Program is running.......")
    username = input('Username:')
    password = getpass.getpass()
    enablepass = input('enable:')
    filepath2 = r'C:\netpy\\'
    if os.path.exists(filepath2):
        message = 'OK,the  "%s" file exists.'
    else:
        message =  "Now, I will create the %s"
        os.makedirs(filepath2)
        
    for ips in open(r'C:\netpy\iplist.txt','r'):
        start_time = datetime.now()
        iplist = ips.replace('\n', '')
        try:
            NetworkDevice(username,password,iplist,enablepass)
        except (EOFError, NetMikoTimeoutException):
            print ('Can not connect to Device')
        except (EOFError, NetMikoAuthenticationException):
            print ('username/password wrong!')
        except (ValueError,NetMikoAuthenticationException):
            print ('enable password wrong!')
            

        print ("Time elapsed: {0}\n".format(datetime.now() - start_time))
        time.sleep(2)