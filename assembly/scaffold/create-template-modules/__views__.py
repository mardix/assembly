# -*- coding: utf-8 -*-
"""
Assembly views

This is the views file. Create all of your view classes in here

## Example

class Index(Assembly):

    # path: /
    # It will match the template at /templates/Index/index.html
    def index(self):
        return "Hello world"

    # path: /about-us
    # It will match the template at /templates/Index/about_us.html
    def about_us(self):
        return 

class Blog(Assembly):

    # path: /blog/
    # It will match the template at /templates/Blog/index.html
    def index(self):
        return "Hello world"

    # path: /blog/posts
    # It will match the template at /templates/Blog/posts.html
    def posts(self):
        return   

class API(Assembly):

    # path: /api/
    # It will return a json

    @response.json    
    def index(self):
        return {
            "name": "Assembly",
            "version": "x.y.z"
        }

    # path: /api/items
    # It will return a json

    @response.json    
    def items(self):
        return {
            "data": {
                "items": [1, 2, 3]
            }
        }

"""

from assembly import (Assembly,
                      asm,
                      models, 
                      request,
                      response,
                      HTTPError)

# ------------------------------------------------------------------------------


@request.route("/%ROUTE%/")
class Index(Assembly):

    def index(self):
        return
