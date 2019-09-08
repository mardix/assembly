# -*- coding: utf-8 -*-
""""
________________________________________________________________________________
FLASIK: https://github.com/mardix/flasik
________________________________________________________________________________

That's the application entry point
"""

from flasik import Flasik

# == Commander ==
# Import commander to use your own command line functions.
# Comment out to omit
import main.cli

# == Projects ==
# a dict with list of applications to load by name
# You can add as many views as you want, containing as many views
# It also allows you to use multiple config env
# Format: `FLASIK_PROJECT=$project_name:$config_env flasik-admin run`
# => FLASIK_PROJECT="default:production" flasik-admin run
# will use the `default` project with `production` __config__

projects = {
    "default": [
        "main"
    ]
}

# == INITIALIZE ==
# Init the application
# 'app' variable is required to use the commander -> flasik
app = Flasik.Initialize(__name__, projects)
