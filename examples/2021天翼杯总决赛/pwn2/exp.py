#!/usr/bin/python
#  -*- coding: utf-8 -*-
import re
import sys
import requests
from pwn import*

host = sys.argv[1]
#PORT = sys.argv[2]
#context(log_level="debug")
#p = process('./pwn')
#libc = ELF('/usr/lib/freelibs/amd64/2.32-0ubuntu3.2_amd64/libc.so.6')

def exp(ip, port):
    # ...
    p.recvuntil("flag")
    testFlag = ("flag" + p.recv()).strip()

    match_group = re.findall("flag{(.*?)}", testFlag)
    flag = match_group[0]

    return flag
    p.interactive()
    
def write_to_flags(d):
    fd = open('./flags', 'ab')
    fd.write(d)
    fd.close()
    
if __name__ == '__main__':
    HOST = host.split(':')[0]
    PORT = int(host.split(':')[1])
    flag = exp(HOST, PORT)
    flag = "flag{"+flag+"}"
    print(flag)
    write_to_flags(flag + '\n')
    print("Pass!")


