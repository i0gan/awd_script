#!/usr/bin/env python3
# Author: i0gan
# A script for awd upload file

from pwn import *
import os

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

elf_path  = 'pwn'
file_name='./upload_file'
LOCAL = 0
LIBC  = 1

if(len(sys.argv) < 2):
    LOCAL = 1
    context.log_level='debug'
else:
    #context.log_level='cratical'
    server_ip = sys.argv[1].split(':')[0]
    server_port = int(sys.argv[1].split(':')[1])

libc_path = './libc.so.6'
#--------------------------func-----------------------------
def db():
    if(LOCAL):
        gdb.attach(io)
def input_code(sz, d):
    sla('$', '1')
    sla(':', str(sz))
    sa(':', d)
    
def upload():
    sleep(1)
    sl('echo "i0gan"')
    ru('i0gan')
    p = '/bin/echo -ne "'
    p += get_file_hex()
    p += '" > ' + file_name
    print(p)
    sl(p)

def get_file_hex():
    fd = open(file_name, 'rb')
    d = fd.read()
    fd.close()
    h = ''
    for c in d:
        h += '\\x'    
        h += "%02x" % c
    return h
    
#--------------------------exploit--------------------------
def exploit():
    li('exploit...')
    upload()
    
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
