# -*- coding: utf-8 -*-
""""
________________________________________________________________________________
Assembly: https://github.com/mardix/assembly
________________________________________________________________________________

Assembly wsgi.py

This your application's object

----------

# PROJECTS

# a dict with list of applications to load by name
# You can add as many views as you want, containing as many views
# It also allows you to use multiple config env
#

# Environment variables
export ASSEMBLY_ENV=Development
export ASSEMBLY_PROJECT=default

"""

from assembly import Assembly

# Import your application CLI
import main.cli

PROJECTS = {
    "default": [
        "main"
    ]
}

"""
----------- Init -----------------------
Initialize the application
the `app` variable is required
"""
app = Assembly.init(__name__, PROJECTS)
