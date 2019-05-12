#! py -2
# -*- coding: utf-8 -*-

import requests


# 漫画柜里自杀岛的网址
url = "https://www.manhuagui.com/comic/4375/"
# 获取url的Response
res = requests.get(url)
try:
    res.raise_for_status()
except Exception as exc:
    print "There is a problem: %s" % (exc)

playFile = open("index.html", "wb")
for chunk in res.iter_content(100000):
    playFile.write(chunk)
# print res.text











