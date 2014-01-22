#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import time
import codecs
import urllib
import markdown
#from HTMLParser import HTMLParser

blog_posts = []
file_path = "contents/"

##class MyHTMLParser(HTMLParser):
#    def __init__(self):
#        HTMLParser.__init__(self)
#        self.is_para = False
#        self.para = u"" 
#    def handle_starttag(self, tag, attrs):
#        if tag == "p":
#            self.is_para = True
#    def handle_data(self, data):
#        if self.is_para:
#            self.para += data
#    def handle_endtag(self, tag):
#        if tag == "p":
#            self.is_para = False

class Articles(object):
    def __init__(self, filename):
        self.name = filename.replace(".md", "");
        self.time, self.title = self.name.split("_") 
        self.ctime = time.ctime(os.path.getctime(file_path + filename))
        self.url = "/blog/" + self.time.replace("-", "/") + "/" + self.title
        
        input_file = codecs.open(file_path + filename, mode = "r", 
                encoding = "utf-8")
        self.html = markdown.markdown(input_file.read(), ['codehilite'])
        loc = self.html.find(u"<!--more-->") + len(u"<!--more-->")
        self.para = self.html[:loc]
        self.para = self.para.replace(u"<!--more-->", 
                u'''<p><a class="btn btn-danger" href= "''' + 
                self.url.decode("utf-8") + 
                u'''" role="button">View details</a></p>''')

#        parser = MyHTMLParser() 
#        parser.feed(self.html)
#        self.para = parser.para[0:200]

def init_list():
    file_list = os.listdir(file_path)

    for each in file_list:
            blog_posts.append(Articles(each)) 

    blog_posts.sort(cmp = lambda x,y:cmp(x.ctime, y.ctime), reverse = True)
