"""
Flasik Views
"""
from flasik import (Flasik,
                   page_attr,
                   config,
                   flash_success,
                   flash_error,
                   abort,
                   request,
                   url_for,
                   redirect,
                   models,
                   utils,
                   paginate,
                   render,
                   decorators as deco
                   )


# ------------------------------------------------------------------------------


class Index(Flasik):
    def index(self):
        page_attr(title="Hello View!")
        return
