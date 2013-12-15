#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import web

from controllers.index import Index
from config.url import urls
from controllers.init import init_list
from controllers.init import blog_posts

init_list()
if __name__ == "__main__":
    application = web.application(urls, globals()).run()
else:
    application = web.application(urls, globals(), autoreload = True).wsgifunc()
