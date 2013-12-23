#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web

from controllers.init import blog_posts
from config.setting import render

class Index:
    def GET(self):
        return render.index(blog_posts, render)

class Contact:
    def GET(self):
        return render.contact()
