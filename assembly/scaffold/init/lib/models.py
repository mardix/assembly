# -*- coding: utf-8 -*-
"""
Assembly: models.py

*This module is loading implicitely by Assembly. Do not import*

Contains applications models and other databases connections.

To setup: `asm gen:sync-models`


## Example 

class MyModel(db.Model):
    name = db.Column(db.String(255), index=True)


## Usage

from assembly import models

Accessor: models.[ClassName]
ie: models.MyModel
-----
"""

from assembly import db

# ------------------------------------------------------------------------------

class Test(db.Model):
    name = db.Column(db.String(255), index=True)

