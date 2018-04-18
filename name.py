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

pages = 9


def getImg(html):
    global pages, path
    pages -= 1
    assert pages>=0, "done"
    pic_url = re.findall('blank.><img src="(.*?)".alt=.*?width', html, re.S)
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
    url = re.findall('<a class="two" href="(.*?)"', html, re.S)[0]
    html = requests.get(url).text
    #getImg(html)
    g = gevent.spawn(getImg, html)
    g.join()

    #print pic_url, '\n\n', "name:",name[0].encode('utf-8').decode('utf-8'), '\n\n', nexturl
    return


if __name__ == '__main__':
    start = time.time()
    url = 'http://www.ifensi.com/list9/1-1-1-1-1-1/10.html'
    html = requests.get(url).text
    #getImg(html)
    g = gevent.spawn(getImg, html)
    g.join()
    print"with gevent use ", time.time()-start # 7.07706308365
    #print"without gevent use ", time.time()-start # 7.84964609146
