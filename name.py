#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 09:58:40 2018

@author: hannah
"""
import requests
import re
import os
path = os.getcwd()
import gevent
import time


def getpages():
    url = 'http://www.ifensi.com/list9/'
    pages = 9
    while(pages!=0):
        html = requests.get(url).text
        getImg(html)

        
        url = re.findall('<a class="two" href="(.*?)"', html, re.S)[0]
        pages -= 1
    return 


def getImg(html):
    global path
    pic_url = re.findall('blank.><img src="(.*?)" alt=.*?width', html, re.S)
    name = re.findall('blank.><img src=".*?alt="(.*?)"', html, re.S)
    
    for i in range(len(pic_url)):
        try:
            pic= requests.get(pic_url[i], timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
            continue
        filepath = os.path.join(path, name[i]+'.jpg')
        fp = open(filepath,'w')
        fp.write(pic.content)
        fp.close()
        i += 1
    
    #print pic_url, '\n\n', "name:",name[0].encode('utf-8').decode('utf-8'), '\n\n', nexturl
    #print len(name), len(pic_url)
    return


if __name__ == '__main__':
    start = time.time()
    getpages()
    #print"with gevent use ", time.time()-start # 10.0935359001
    print"without gevent use ", time.time()-start # 