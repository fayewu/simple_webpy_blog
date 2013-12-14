#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web
import urllib

from controllers.init import blog_posts
from config.setting import render

class Blog:
    def GET(self, url):
        url = urllib.unquote(url)
        for each in blog_posts:
            if url == each.title_url:
                break
        return render.blog(each)

