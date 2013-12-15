#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web
import urllib

from controllers.init import blog_posts
from config.setting import render

class Blog:
    def GET(self, url): 
        url = url.encode("utf-8")
        url = "/blog/" + url
        for each in blog_posts:
            if url == each.url:
                break
        return render.blog(each)

