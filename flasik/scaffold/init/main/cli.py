# -*- coding: utf-8 -*-
"""
cli.py
Place all your command line functionalities in here.
Execute your commands in as `flasik $command-name`

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

# 3
run > 'flasik' to view all of your commands

"""

from flasik.cli import (command, option, argument, click)
from flasik import db 

@command()
def setup():
    """ Application initial setup """
    click.echo("This is a setup!")

