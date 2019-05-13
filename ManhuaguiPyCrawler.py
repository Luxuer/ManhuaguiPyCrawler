#! py -2
# -*- coding: utf-8 -*-

import requests

# 漫画柜里自杀岛的网址
url = "https://www.manhuagui.com/comic/4375/37875.html" # 漫画第一页
# url = "https://www.manhuagui.com/comic/4375/" # 下载漫画介绍页
# 获取url的Response
res = requests.get(url)
try:
    res.raise_for_status()
except Exception as exc:
    print "There is a problem: %s" % (exc)

# 把大古熬成汤(误), 正确是把文本变成汤
import bs4
soup = bs4.BeautifulSoup(res.text, "lxml")

# 将html写入文件
import codecs
playFile = codecs.open("001.html", "w", "utf-8")
# playFile = codecs.open("index.html", "w", "utf-8")
playFile.write(soup.prettify())

# print res.text











