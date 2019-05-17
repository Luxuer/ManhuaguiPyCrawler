
'''
撰寫 阿東 於 2018-08-01	2018-08-13 python爬蟲
學了python總要有些實戰項目來練練身手，之前已經做過股票資料的爬蟲，今天就來嘗試使用python漫畫爬蟲。

網路上有很多的漫畫爬蟲，但大多數(應該說全部哈哈)都是爬漫畫地址的jpg檔案，而阿東我最喜歡的漫畫網站，
固然是manhuagui(相信多數有看漫畫的台灣朋友應該跟我差不多)，而該網站的漫畫圖片是採用動態載入的，就算利用右鍵檢查元素，
發現漫畫網址，也無法二次打開圖片， 因此本文採用完全selenium加上phantom JS 來模擬瀏覽器的操作，並透過截圖方式將漫畫一頁一頁的保存。

以下是程式碼的分享(若要轉載請留言告知):
'''


#! Python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 12:40:16 2018

@author: alwaysmle
"""

from PIL import Image
from selenium import webdriver 
import requests
import time
from bs4 import  BeautifulSoup
import os
import shutil



comic_link = 'https://tw.manhuagui.com/comic/18847/'        #放要抓的漫畫首頁的地方 !!!!!!!!!!



headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }

def get_jpg(my_url,name):
    url='https://tw.manhuagui.com'+my_url
    browser.get(url)
    browser.implicitly_wait(15)  #等待讀取完畢
    time.sleep(3)
    pageNum = len(browser.find_elements_by_tag_name('option')) #透過有的option選項 判斷頁數
    
    for i in range(pageNum):
        if i > 0:
            browser.find_element_by_id("next").click() #點下一頁
        browser.get_screenshot_as_file('screem_Name.png') #螢幕截圖  為了給之後修圖用
        browser.implicitly_wait(20)  #等待讀取完畢
        time.sleep(4)
        imgelement = browser.find_element_by_xpath('//*[@id="mangaBox"]/img')  #找到放置漫畫的html
        location = imgelement.location  # 獲取圖片中xy座標
        size = imgelement.size  # 獲取圖片長寬
        cutrange = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                            int(location['y'] + size['height']))
        ii = Image.open('screem_Name.png')  # 打開截圖
        newimg = ii.crop(cutrange)  # 使用Image的crop函数，從截圖中選取需要的區域
        print(i+1)
        pic_name=name+'-'+str(i+1)+'.png'
        newimg.save(pic_name)#保存新圖片
        shutil.move(pic_name, './'+comic_name) #將圖片一道資料夾底下

        
def get_chapters_url(re_link):  #獲得漫畫章節網址url
    chapter_link_list = {}
    re_request = requests.get(re_link,headers = headers)
    if re_request.status_code != 200:
        print ('Get Re Manhua Page Failed')
        exit(1)
    else:
        soup = BeautifulSoup(re_request.text,'html.parser')
        chapter_list = soup.find('div',class_='chapter-list cf mt10')
        for ul in chapter_list.contents:
            for li in ul.contents:
                chapter_link_list[li.a['title']] = li.a['href']
    return chapter_link_list

        

chapter_link=get_chapters_url(comic_link)
sort_link=sorted(chapter_link.keys())  #排序漫畫集數
len_link=len(sort_link)  #確定他有幾回


for i in range(len_link):
    url=chapter_link[sort_link[i]]
    name=sort_link[i].split(' ')[0]
    try:   #放這麼多層是因為這樣絕對部會噴bug    原因不知  或許phantomJS 內有bug  已經停止更新  
        get_jpg(url,name)
    except:
        try:
            browser=webdriver.PhantomJS()
            get_jpg(url,name)
        except:
            try:
                get_jpg(url,name)
            except:
                browser=webdriver.PhantomJS()
                get_jpg(url,name)

browser.quit()






