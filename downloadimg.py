#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 09:34:05 2018

@author: hannah
"""

import re
import requests
import numpy as np
import urllib2

#word = raw_input("输入关键字搜索图片: ")

url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1523615906626_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E4%B8%AD%E5%9B%BD90%E5%90%8E%E5%AE%9E%E5%8A%9B%E5%A5%B3%E6%BC%94%E5%91%98'
#proxies = { "http": "http://504.curi.hk:1080", "https": "https://504.curi.hk:1080" }   

html = requests.get(url).text

start_img_index = 304

def getImg(html):
    pic_url = re.findall('"thumbURL":"(.*?jpg)","replace', html,)
    i = start_img_index
    for each in pic_url:
        print each
        try:
            pic= requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
            continue
        string = '/home/hannah/Desktop/train/'+str(i) + '.jpg'
        fp = open(string,'w')
        fp.write(pic.content)
        fp.close()
        i += 1
            
    return 

if __name__ == '__main__':
    getImg(html)
