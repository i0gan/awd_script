# awd_script



AWD批量攻击脚本(Web/Pwn通用)，通过bash编写，远程信息采用参数传入exp，通过多进程方式实现同时攻打，阻塞超时自动结束进程。

各位师傅，下面批量脚本已运用在多次线下awd比赛中，其中web/pwn都运用过，各位web|| pwn师傅给个星是对我最大的支持，谢谢！



文件目录

```
.
├── init : 为每个题目创建文件夹和初始化文件
├── init_hosts : 规划队伍ip和端口
├── attack : 批量攻击脚本
├── exp : awd pwn exp脚本 [自己使用]
├── hosts: 攻击靶机远程信息，ip:port
├── README.md
├── submit_flag: 批量提交flag脚本
├── upload: 文件上传脚本 [PWN使用]
└── upload: 文件上传脚本 [PWN使用]

```



## 批量如何使用？

attack脚本就是批量攻击脚本，攻击脚本如下。

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
        timeout --foreground $run_time python ./exp $line & # 调用exp，传入远程信息。
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
timeout --foreground $run_time python ./exp $line &
```

而$line是从hosts文件取出来的单行信息，用于给exp传入远程host信息。

hosts文件格式是 ip:port

```
172.20.5.1:6022
172.20.5.2:6022
172.20.5.3:6022
172.20.5.4:6022
172.20.5.5:6022
172.20.5.6:6022
```

在exp中处理接受一下参数即可，如下。

```python
server_ip = sys.argv[1].split(':')[0]
server_port = int(sys.argv[1].split(':')[1])
```

接受到的信息，在细微调整一下exp即可。

攻击成功后，在exp中将flag写入flags文件中，方便根据平台接口实现批量提交flag。



[PWN] 拿到shell后建议采用如下方式写入flags

```python
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
    fd.write(d)
    fd.close()

def write_to_logs(d):
    fd = open('./logs', 'ab')
    fd.write(d)
    fd.close()
```

Web的话师傅们自行调整下。

