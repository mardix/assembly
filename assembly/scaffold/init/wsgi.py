# -*- coding: utf-8 -*-
"""
Assembly

https://github.com/mardix/assembly
--------------------------------------------------------------------------------

"wsgi.py" is the application object. It's required by Assembly.

It sets up and initialize all the views per application

--------------------------------------------------------------------------------

# Environment variables

export ASSEMBLY_ENV=Development
export ASSEMBLY_APP=default

## ASSEMBLY_APP
By default, Assembly will attempt to load the 'default' app. 
To specify a different app, set the environment variable 'ASSEMBLY_APP'
to the name of the app to use
ie: 'export ASSEMBLY_APP=default'

## ASSEMBLY_ENV
By default, Assembly will attempt to load the 'Development' config object from './config.py'
To specify a different environment, set the environment variable 'ASSEMEBLY_ENV'
to the environment class name 
ie: 'export ASSEMBLY_ENV=Production'
"""

"""
Import the base Assembly
"""
from assembly import Assembly

"""
Import scripts to enable their command line interface
"""
import run.scripts

"""
APPS = {}
a dict with list of apps to load by name
You can add as many apps as you want per application.
Set the environment variable 'ASSEMBLY_APP' to the name of the app to use
ie: 'export ASSEMBLY_APP=default'
"""

APPS = {
    "default": [
        "views"
    ]
}

"""
Initialize the application
the 'app' variable is required
"""
app = Assembly.init(__name__, APPS)
