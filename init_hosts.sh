#!/bin/bash

ip_start=101
ip_end=110
ip=10.1.
port=8080

rm hosts 2> /dev/null
for((i=$ip_start; i < $ip_end; i++));
do
    echo $ip$i".2":$port >> hosts
done
