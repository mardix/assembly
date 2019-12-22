# -*- coding: utf-8 -*-
"""
Assembly: %MODULE_NAME%.py
"""

from assembly import (Assembly,
                      asm,
                      models, 
                      request,
                      response,
                      HTTPError)

# ------------------------------------------------------------------------------


@request.route("/%ROUTE_NAME%/")
class Index(Assembly):

    def index(self):
        return
