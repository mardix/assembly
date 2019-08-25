# -*- coding: utf-8 -*-
"""
Flasik: models.py

Contains applications models and other databases connections.

Do not `import`. This module is loaded implicitely by Flasik

To setup: `flasik-admin sync-models`

-----
# ActiveAlchemy, 

Accessor: models.[ClassName]
ie: models.MyModel

class MyModel(db.Model):
    ...

-----

# Redis
Redis can also be connected in here

> db.connect_redis(name='rdb', url=get_config("REDIS_URL"))

Accessor: db.redis.[name]
ie: db.redis.rdb.set("key", "value")
"""

from flasik import db, get_config

# --------------------------------------------------------------------------

"""
Redis Connection
"""
# db.redis_connect('db', get_config("REDIS_URL"))

# --------------------------------------------------------------------------

"""
ActiveAlchemy Models
"""

class Test(db.Model):
    name = db.Column(db.String(255), index=True)


