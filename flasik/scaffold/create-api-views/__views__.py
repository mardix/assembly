# -*- coding: utf-8 -*-
"""
Flasik Views
"""
from flasik import (Flasik,
                    set_page_context,
                    get_config,
                    abort,
                    url_for,
                    redirect,
                    models,
                    request,
                    response,
                    functions,
                    utils)

# ------------------------------------------------------------------------------

@request.route("/%ROUTE%/")
class Index(Flasik):

    @response.cors()
    @response.json 
    def index(self):
        return {}

    @response.cors()
    @response.json 
    def api(self):
        return {
            "date": functions.utc_now(),
            "location": "NC"
        }
