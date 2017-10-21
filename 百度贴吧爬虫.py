#-*- coding:utf-8 -*-
''''
author: qirui_han
'''

import urllib
import urllib2
import re

class Tool:
    removeImg = re.compile('<img.*?>| {1,}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return  x.strip()

class BDTB:
    def __init__(self,baseURL,seeLZ,floorTag):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self,pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError ,e :
            if hasattr(e,"reason"):
                print u"突然出错了呢，嗯，错误原因是....是:",e.reason
                return NOne

    def getTitle(self,page):
        pattern = re.compile('<div class="core_title.*?>.*?<h1.*?>(.*?)</h1>',re.S)
        result =re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            print "Error!"
            return None


    def getPageNum(self,page):
        pattern = re.compile('<ul class="l_posts_num.*?</span>.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            print "Error!"
            return None


    def getContent(self,page):
        pattern = re.compile('<div id="post_content.*?>.*?</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in  items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + '.txt',"w+")
        else:
            self.file = open(self.defaultTitle + '.txt',"w+")

    def writeData(self,contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) +  u"-------------------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "抱歉，URL好像已经失效了呢！请重新再输入一个吧："
            return
        try:
            print "这篇帖子一共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print "写入异常了呢，嗯。。。。原因是" + e.message
        finally:
            print "写入完成啦！"





print u"请输入帖子编号，如http://tieba.baidu.com/p/5339373347  中的 5339373347 这串字数字 "
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只看楼主发言呢？是请输入1，否请输入0\n")
floorTag = raw_input("是否写入楼层信息呢？ 是输入1，否输入0\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()