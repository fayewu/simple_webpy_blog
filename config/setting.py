#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web

from url import urls

web.config.debug = False
app = web.application(urls, globals()).wsgifunc()

#web.config_session = session

#render_login = web.template.render("templates/", globals = {'context':session})
render = web.template.render("templates/", globals = {'context':session})
web.template.Template.globals['render'] = render
