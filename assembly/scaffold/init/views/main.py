# -*- coding: utf-8 -*-
"""
Assembly views.py
"""

from assembly import (Assembly,
                      asm,
                      date,
                      models,
                      request,
                      response,
                      HTTPError)

# ------------------------------------------------------------------------------


class Index(Assembly):

    def index(self):
        return

    @request.cors
    @response.json
    def api(self):
        return {
            "date": date.utcnow(),
            "description": "API Endpoint with CORS and JSON response"
        }

    @response.json
    @response.cache(timeout=10)
    def cached(self):
        return {
            "description": "This is a cached endpoint",
            "date": date.utcnow(),
        }


    def error(self):
        """
        Accessing /error should trigger the error handlers below
        """
        raise HTTPError.NotFound()
