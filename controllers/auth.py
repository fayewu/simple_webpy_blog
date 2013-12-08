#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web

from config.setting import render_login

def logged():
    if web.config_session.login == 1:
        return True
    else:
        return False

class Login: 
    def GET(self):
        if logged():
            return web.seeother("/status/login_true") 
        else:
            return render_login.login()
    def POST(self):
        user_data = web.input() 
        var = dict(username = user_data.username)
        var["passwd"] = user_data.passwd
        result = db.select("user", var, where = "username = $username and passwd = $passwd").list()

        if result == []:
            raise web.seeother("/status/login_false") 
        else:
            session.login = 1
            raise web.seeother("/status/login_true")

class Reset():
    def GET(self):
        web.config_session.login = 0
        web.config_session.kill()

class Status:
    def GET(self, flag):
        return render.status(flag)
