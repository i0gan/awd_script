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
