#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web
import MySQLdb

from controllers.auth import Login, Reset
from controllers.index import Index
from config.setting import app
from config.url import urls

if __name__ == "__main__":
    app.run()
