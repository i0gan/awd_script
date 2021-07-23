#!/usr/bin/python
import string
import time

with open('./flags', 'r') as f:
    flag = 0
    data = f.readlines()
    All = len(data)
    for line in data:
        if len(line) > 32:
            flag += 1
print("get %d flags"%flag)
print("succes %.2lf "%(flag/All*100) + "\n")

with open('./all_flags', 'r') as fa:
    flag = 0
    data = fa.readlines()
    All = len(data)
    for line in data:
        if len(line) > 32:
            flag += 1

print("all %d flags"%flag)
print("all succes %.2lf "%(flag/All*100))
