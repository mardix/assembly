# -*- coding: utf-8 -*-
"""
Flasik Views
"""
from flasik import (Flasik,
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
        return {
            "name": "API Endpoint"
        }

    @response.cors()
    @response.json 
    def info(self):
        return {
            "date": functions.utc_now()
        }
