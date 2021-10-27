#!/usr/bin/env python3
# A script for awd exp

from pwn import *
import os
import sys

ip = server_ip = sys.argv[1].split(':')[0]
port = int(sys.argv[1].split(':')[1])

io = remote(ip, port)

r   =  lambda x : io.recv(x)
ra  =  lambda   : io.recvall()
rl  =  lambda   : io.recvline(keepends = True)
ru  =  lambda x : io.recvuntil(x, drop = True)
s   =  lambda x : io.send(x)
sl  =  lambda x : io.sendline(x)
sa  =  lambda x, y : io.sendafter(x, y)
sla =  lambda x, y : io.sendlineafter(x, y)
ia  =  lambda : io.interactive()
c   =  lambda : io.close()
li    = lambda x : log.info('\x1b[01;38;5;214m' + x + '\x1b[0m')

elf_path  = './pwn'
LOCAL = 1
LIBC  = 0

if(len(sys.argv) < 2):
    LOCAL = 1
    context.log_level='debug'
else:
    context.log_level='critical'
    server_ip = sys.argv[1].split(':')[0]
    server_port = int(sys.argv[1].split(':')[1])

libc_path = './libc.so.6'
#--------------------------func-----------------------------
def db():
    if(LOCAL):
        gdb.attach(io)

def cat_flag():
    flag_header = b'flag{'
    sleep(1)
    sl('cat flag')
    ru(flag_header)
    flag = flag_header + ru('}') + b'}'
    write_to_flags(flag + b'\n')
    write_to_logs(b'\nexploited: ' + server_ip.encode() + b':' + str(server_port).encode() + flag)
    exit(0)

def write_to_flags(d):
    fd = open('./flags', 'ab')
    fd.write(d + b'\n')
    fd.close()
    
#--------------------------exploit--------------------------
def exploit():
    li('exploit...')
    
def finish():
    ia()
    c()

#--------------------------main-----------------------------
if __name__ == '__main__':
    if LOCAL:
        elf = ELF(elf_path)
        if LIBC:
            libc = ELF(libc_path)
            io = elf.process(env = {"LD_PRELOAD" : libc_path})
        else:
            io = elf.process()
    else:
        elf = ELF(elf_path)
        io = remote(server_ip, server_port)
        if LIBC:
            libc = ELF(libc_path)
    exploit()
    finish()

