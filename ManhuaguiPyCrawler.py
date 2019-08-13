#! py -2
# -*- coding: utf-8 -*-

import os
import requests
from selenium import webdriver 
import bs4
import time


def get_chapter_urls(url, headers):  #獲得漫畫章節網址url
    chapter_urls = {}
    headers['Referer'] = url
    res = requests.get(url,headers = headers)
    try:
        res.raise_for_status()
    except Exception as exc:
        print "There is a problem: %s" % (exc)

    soup = bs4.BeautifulSoup(res.text,'lxml')
    # # 章节列表的格式如下: 
    # ``` html
    # <div class="chapter-list cf mt10" id="chapter-list-1">
    #   <ul style="display: block;">
    #       <li>
    #           <a href="/comic/4375/37952.html" title="第078回" class="status0" target="_blank">
    #               <span>第078回<i>20p</i></span>
    #           </a>
    #       </li>
    #       <li>
    #           ...
    #       </li>
    #       ...
    #   </ul>
    #   <ul style="display: none;">
    #       <li>
    #           <a href="/comic/4375/258627.html" title="第168回 我们选择活下去" class="status0" target="_blank">
    #               <span>第168回我…<i>30p</i></span>
    #           </a>
    #       </li>
    #       <li>
    #           ...
    #       </li>
    #       ...
    #   </ul>
    # </div>
    # ```
    
    chapter_list = soup.find('div',class_='chapter-list cf mt10')
    for ul in chapter_list.contents:
        for li in ul.contents:
            chapter_urls[li.a['title']] = li.a['href']
    return chapter_urls

manhuagui_url = "https://www.manhuagui.com" # manhuagui首页网址
comic_url = "https://www.manhuagui.com/comic/4375/" # 目标漫画介绍页
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', 
'Referer':''}

comic_dir = "SuisideIsland" # 漫画存放目录
# 创建目录
if not os.path.exists(comic_dir): 
    os.makedirs(comic_dir) 


chapter_urls = get_chapter_urls(comic_url, headers)
sorted_chapter_names = sorted(chapter_urls.keys())  #排序漫畫集數
chapter_num = len(sorted_chapter_names)  #確定他有幾回
# # 按下开始阅读按钮
# ``` html
# <div class="book-btn">
#   <a href="/comic/4375/37875.html" target="_blank" title="第001回" class="btn-read">开始阅读</a>
#   <a href="javascript:;" id="toChapter" class="btn-chapter" title="章节列表">章节列表</a>
#   <a href="javascript:;" id="toFav" class="btn-fav" title="加入收藏">加入收藏</a>
#   <a href="javascript:;" id="toComment" class="btn-cmt" title="我要吐槽">我要吐槽</a>
# </div>
# ```
driver = webdriver.Chrome() # 打开浏览器
driver.implicitly_wait(15) 
driver.get(comic_url) # 访问漫画介绍页
print driver.current_url
driver.find_element_by_class_name('btn-read').click() # 点击开始阅读按钮
time.sleep(10) # 等待打开第一回
window_handles = driver.window_handles # 获取浏览器各个窗口的句柄
driver.switch_to.window(window_handles[1]) # 切换到漫画第一回的窗口
print driver.current_url

for i in range(chapter_num):
    chapter_name = sorted_chapter_names[i]
    print "Chapter name: %s" % (chapter_name) # 章节名
    chapter_url = manhuagui_url + chapter_urls[chapter_name] # 该章节对应的网址
    print "Chapter url: %s" % (chapter_url) # 章节网址
    headers['Referer'] = chapter_url # 更新该章节对应的headers
    page_num = len(driver.find_elements_by_tag_name('option')) # 页数
    print "Page number: %s" % (page_num)
    for j in range(page_num):
        # 找到图片链接
        element = driver.find_element_by_id('mangaFile')
        image_url = element.get_attribute('src')
        # 下载图片
        print "Downloading image: %s" % (image_url)
        res = requests.get(image_url, headers=headers)
        try:
            res.raise_for_status()
        except Exception as exc:
            print "There is a problem: %s" % (exc)
        # 保存图片到./comic_dir/chapter_name/下
        # 在./comic_dir下创建目录chapter_dir
        chapter_dir = os.path.join(comic_dir, chapter_name)
        if not os.path.exists(chapter_dir): 
            os.makedirs(chapter_dir) 

        str_split = os.path.basename(image_url).split('.') # 将image_url的basename按照'.'号分开
        image_name = str_split[0]+'.'+str_split[1] # 构造图片文件名字
        image_path = os.path.join(chapter_dir, image_name) # 构造图片文件路径
        image_file = open(image_path, 'wb') # 打开图片文件
        # 将图片保存到image_path
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()
        # 判断该点下一页还是下一个章节
        if j == page_num-1: # 如果到了该章节最后一页
            driver.find_element_by_css_selector("[class='btn-red nextC']").click() # 点下一章节
            time.sleep(10) # 等待章节切换
        else:
            driver.find_element_by_id("next").click() # 点下一页

# 下面都是别人写的代码, 仅供参考
# driver = webdriver.Chrome() # 打开浏览器
# driver.get(url) # 浏览漫画第一页
# driver.implicitly_wait(15)  #等待讀取完畢
# time.sleep(3)

# page_num = len(driver.find_elements_by_tag_name('option')) #透過有的option選項 判斷頁數
# print "page num: %s" % (page_num)
# driver.find_element_by_id("next").click() # 点下一页, 到达第二页
# time.sleep(1)
# driver.find_element_by_id("prev").click() # 回到第一页

# charpter_count = 1
# page_num -= 1
# for i in range(page_num):
#     # 找到图片链接
#     element = driver.find_element_by_id('mangaFile')
#     image_url = element.get_attribute('src')
#     # 下载图片
#     print "Downloading image %s" % (image_url)
#     res = requests.get(image_url, headers=headers)
#     try:
#         res.raise_for_status()
#     except Exception as exc:
#         print "There is a problem: %s" % (exc)
#     # 保存图片到./comic_dir
#     str_split = os.path.basename(image_url).split('.')
#     image_file = open(os.path.join(comic_dir, str_split[0]+'.'+str_split[1]), 'wb')
#     for chunk in res.iter_content(100000):
#         image_file.write(chunk)
#     image_file.close()
#     driver.find_element_by_id("next").click() # 点下一页
# driver.find_element_by_css_selector("[class='btn-red nextC']").click() # 点下一章节

# content = driver.page_source
# # print content
# soup = bs4.BeautifulSoup(content, 'lxml')
# elements = soup.select('img[id="mangaFile"][alt]')
# image_url = elements[0].get('src')

# print "Downloading image %s" % (image_url)
# res = requests.get(image_url)
# try:
#     res.raise_for_status()
# except Exception as exc:
#     print "There is a problem: %s" % (exc)

# image_file = open(os.path.join('SuisideIsland'))
# <script type="text/javascript" src="https://cf.hamreus.com/scripts/core_C0683FDCDEE69940232A703BDEB0F64F.js"></script>





# # 声明一个司机，司机是个Chrome类的对象
# driver = webdriver.Chrome()
 
# # 让司机加载一个网页
# driver.get("http://demo.ranzhi.org")
 
# # 给司机3秒钟去打开
# time.sleep(3)
 
# # 开始登录
# # 1. 让司机找用户名的输入框
# we_account = driver.find_element_by_css_selector('#account')
# we_account.clear()
# we_account.send_keys("demo")
 
# # 2. 让司机找密码的输入框
# we_password = driver.find_element_by_css_selector('#password')
# we_password.clear()
# we_password.send_keys("demo")

# # 3. 让司机找 登录按钮 并 单击
# driver.find_element_by_css_selector('#submit').click()
# time.sleep(3)




