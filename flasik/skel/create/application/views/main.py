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


class Index(Flasik):

    def index(self):
        set_page_context(title="Hello World", description="Under Construction")
        return

    @response.cors()
    @response.json 
    def api(self):
        return {
            "date": functions.utc_now(),
            "location": "NC"
        }
