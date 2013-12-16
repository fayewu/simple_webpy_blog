#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import time
import codecs
import urllib
import markdown

blog_posts = []
file_path = "contents/"

class Articles(object):
    def __init__(self, filename):
        self.name = filename.replace(".md", "");
        self.time, self.title = self.name.split("_") 
        self.ctime = time.ctime(os.path.getctime(file_path + filename))
        self.url = "/blog/" + self.time.replace("-", "/") + "/" + self.title
        
        input_file = codecs.open(file_path + filename, mode = "r", 
                encoding = "utf-8")
        self.html = markdown.markdown(input_file.read())

def init_list():
    file_list = os.listdir(file_path)

    for each in file_list:
            blog_posts.append(Articles(each)) 

    blog_posts.sort(cmp = lambda x,y:cmp(x.ctime, y.ctime), reverse = True)
