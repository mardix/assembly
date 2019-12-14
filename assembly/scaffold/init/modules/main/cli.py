# -*- coding: utf-8 -*-
"""
cli.py
Place all your command line functionalities in here.
Execute your commands in as `asm $command-name`

=== Example ===

# 1
@command
def hello():
  print("Hello world!")

# run > asm hello

# 2
@command('do-something')
@argument(name)
def do_something(name):
  print("Hello %s" % name)

# run > asm do-something Mardix

# 3
run > 'asm' to view all of your commands

"""

from assembly.cli import (command, option, argument, click)
from assembly import db 

@command()
def setup():
    """ Application initial setup """
    click.echo("This is a setup!")

