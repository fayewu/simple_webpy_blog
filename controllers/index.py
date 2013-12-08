#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web

from config.setting import render

class Index:
    def GET(self):
        return render.index()
