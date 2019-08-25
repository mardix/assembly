# -*- coding: utf-8 -*-
""""
________________________________________________________________________________
FLASIK: https://github.com/mardix/flasik
________________________________________________________________________________

That's the application's entry point
"""

from flasik import Init


# == Commander ==
# Import commander to use your own command line functions.
# Comment out to omit
import application.commander

# == Views ==
# a dict with list of views to load by name
# ie: `flasik=main flasik-admin run` will serve all the views in the `main` list
# Views are placed in application/views directory, and should be listed as string
# without the `.py`
# You can add as many views as you want, containing as many views
# It also allows you to use multiple config env
# ie: `flasik=main:production flasik-admin run` will use the `main` project with
# `production` config


views = {
    "main": [
        "main"
    ]
}

# To load vendor packages
__views = {
    "main": {
        "views": [
            "main"
        ],
        "vendors": [
            ("a.vendor.package.path", {}) # (package_name<string>, config{any})
        ]
    }
}


# == INIT ==
# Init the application
# 'app' variable is required to use the commander -> flasik
app = Init(__name__, views)
