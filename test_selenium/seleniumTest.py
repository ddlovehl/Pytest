from selenium import webdriver
import time
from test_selenium.logUtils import initLog
import logging
import os


initLog()
################切换句柄start#########################

def switch_handle(driver,curr_handle):
    for handle in driver.window_handles:
        if handle != curr_handle:
            driver.switch_to.window(handle)
            logging.info("切换到句柄title:" + driver.title)
    return
################切换句柄end#########################


################爬取小说end#########################
def spdTxt(txtId):

    txt={}   #存储变量
    txt['title']=''   #小说标题
    txt['id']=txtId   #小说编号
    txt['author']=''  #作者
    txt['intro'] = ''  #小说简介

    browser = webdriver.Chrome()
    logging.info("打开电子书id:%s" % txt['id'])
    browser.get("http://book.km.com/shuku/%s.html" % txt['id'])    # 打开电子书
    ele = browser.find_element_by_css_selector("#xtopjsinfo > div.container.clearfix > div > div.col_a > div.abook.clearfix > div.tit_bg > h2")
    txt['title'] = ele.text
    ele = browser.find_element_by_css_selector("#xtopjsinfo > div.container.clearfix > div > div.col_a > div.abook.clearfix > div.tit_bg > div > span.author > a")
    txt['author'] = ele.text
    ele = browser.find_element_by_css_selector("#xtopjsinfo > div.container.clearfix > div > div.col_a > div.abook.clearfix > div.summary > p.desc")
    txt['intro'] = ele.text

    ###打开小说文件写入小说相关信息
    if os.path.exists('{0:0>8}-{1}.txt.download'.format(txt['id'], txt['title'])):
        os.remove('{0:0>8}-{1}.txt.download'.format(txt['id'], txt['title']))
    fo = open('{0:0>8}-{1}.txt.download'.format(txt['id'], txt['title']), "ab+")
    fo.write((txt['title'] + "\r\n").encode('UTF-8'))
    fo.write(("\t\t\t--作者：" + txt['author'] + "\r\n").encode('UTF-8'))
    fo.write(("*******简介*******\r\n").encode('UTF-8'))
    fo.write(("\t" + txt['intro'] + "\r\n").encode('UTF-8'))
    fo.write(("******************\r\n").encode('UTF-8'))
    ###进入阅读页面
    browser.find_element_by_id("start_read").click()   #点击开始阅读
    time.sleep(3)  # 休眠3秒
    switch_handle(browser, browser.current_window_handle)  # 切换到当前句柄
    ###循环翻页获取内容
    i = 0
    while(1):
        try:
            i = i + 1;
            # 获取章节标题 章节内容
            ele = browser.find_element_by_css_selector("#xtopjsinfo > div.container > div.article > div > div.article-title > h1")  #章节标题
            sub_title = ele.text
            # 获取章节内容
            ele = browser.find_element_by_css_selector("#xtopjsinfo > div.container > div.article > div > div.article-body")
            sub_body = ele.text

            # 以二进制写入章节题目
            fo.write(('\n\n\n\r' + sub_title + '\r\n').encode('UTF-8'))
            # 以二进制写入章节内容
            fo.write((sub_body).encode('UTF-8'))
            logging.info('[%s]章节：[%s]' % ((txt['title'],sub_title)))

            # 获取下一章按钮
            ele = browser.find_element_by_css_selector("#xtopjsinfo > div.container > div.article > div > div.article-page > a.article-page-next")
            eleClass = ele.get_attribute("class")
            if eleClass.count('disabled')>0:# 如果没有下一章
                logging.info('编号：[%s],小说名：[%s]下载完成'%(txt['id'],(txt['title'])))
                break
            #点击下一章
            ele.click()
            time.sleep(2)  # 休眠3秒
        except:
            logging.info('编号：[%s],小说名：[%s]下载失败' % (txt['id'], (txt['title'])))
    fo.close()
    if os.path.exists('{0:0>8}-{1}.txt'.format(txt['id'], txt['title'])):
        os.remove('{0:0>8}-{1}.txt'.format(txt['id'], txt['title']))
    os.rename('{0:0>8}-{1}.txt.download'.format(txt['id'], txt['title']),'{0:0>8}-{1}.txt'.format(txt['id'], txt['title']))
    browser.quit()   #关闭浏览器

spdTxt("1486066")
