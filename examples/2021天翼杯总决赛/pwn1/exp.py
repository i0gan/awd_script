#! /usr/bin/python2
from pwn import *
from sys import *

#context.log_level = 'debug'
#context.log_level = 'critical'
context.terminal = ['tmux', 'splitw', '-h']
LOCAL = 0
#if(LOCAL == 0):
    #if(len(argv) < 3):
    #    print('Usage: ./exp.py [host] [port]')
    #    exit(-1)

host = argv[1]
    #port = int(argv[2])

elf = ELF('./ezcmd')

def exp(io):
    p = 'payload'
    io.send(p)
    #io.interactive()
    flag = None
    flag = io.recvuntil('}')


    return flag
def write_to_flags(d):
    fd = open('./flags', 'ab')
    fd.write(d)
    fd.close()

flag = b''
if(LOCAL):
    io = elf.process()
else:
    io = remote(host.split(':')[0], int(host.split(':')[1]))
    #io = remote(host, port)

flag = exp(io)
flag = flag.decode()
print(flag)
write_to_flags(flag + '\n')
io.close()
