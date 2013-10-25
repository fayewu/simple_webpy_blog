#!/usr/bin/env python
#-*- coding: utf-8 -*-

path = "controllers."
urls = (
        "/", "Index",
        "/status/(.*)", path + "Status",
        "/login", path + "auth.Login",
        "/reset", path + "auth.Reset",
        "/register", path + "Register"
        )
