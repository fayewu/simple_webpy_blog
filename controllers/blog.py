#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web

from controllers.init import blog_posts
from config.setting import render

class Blog:
    def GET(self, url):
        url = "/blog/" + url 
        for each in blog_posts:
            if url == each.url:
                break
        return render.blog(each)

