# -*- coding: utf-8 -*-
"""
Commander.py
Place all your command line functionalities in here.
Execute your commands in as `flasik $command-name`

Documentation: https://click.palletsprojects.com/

=== Example ===

# 1
@command
def hello():
  print("Hello world!")

# run > flasik hello

# 2
@command('do-something')
@argument(name)
def do_something(name):
  print("Hello %s" % name)

# run > flasik do-something Mardix

"""

from flasik.commander import (command, option, argument, click)
from flasik import models

@command()
def setup():
    """ Application initial setup """
    click.echo("This is a setup!")

