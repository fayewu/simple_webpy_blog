#!/usr/bin/env python
#-*- coding: utf-8 -*-

import web

from url import urls

web.config.debug = False

render = web.template.render("templates/", globals = {})
web.template.Template.globals['render'] = render
