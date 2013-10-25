#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web
import MySQLdb

from auth  import Login, Reset

urls = (
        "/", "Index",
        "/status/(.*)", "Status",
        "/count", "Count",
        "/login", "Login",
        "/Reset", "Reset",
        "/register", "Register"
        )

web.config.debug = False
app = web.application(urls, globals())
db = web.database(dbn = "mysql", user = "faye", pw = "wufeishizhu.", 
        db = "web_test");
store = web.session.DBStore(db, "sessions")
session = web.session.Session(app, store, initializer={'login': 0})
web.config_session = session
render = web.template.render("templates/", globals={'context':session})

class Index:
    def Get(self):
        return render.index()
        
class Status:
    def GET(self, flag):
        return render.status(flag)

#class login:
#    def POST(self):
#        user_data = web.input()
#        result = db.select("user", dict(name=user_data.name), 
#                    where = "name = $name").list()
#        if result == []:
#            raise web.seeother("/status/login_false") 
#        else:
#            raise web.seeother("/status/login_true")
#
#class register:
#    def POST(self):
#        user_data = web.input()
#        try:
#            result = db.insert("user", name = user_data.name, 
#                    passwd = user_data.passwd)
#        except IntegrityError, e:
#            raise web.seeother("/status/register_false") 
#        except BaseException, e:
#            raise web.seeother("/status/register_false")
#        else:

if __name__ == "__main__":
    app.run()
