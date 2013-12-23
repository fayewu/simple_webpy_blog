#!/usr/bin/env python
#-*- coding: utf-8 -*-

path = "controllers."
urls = (
        "/", path + "index.Index",
        "/blog/(.*)", path + "blog.Blog",
        "/contact", path + "index.Contact",
        "/work", path + "index.Work"
        )
