
## Overview

Assembly uses `flask-caching` to cache the endpoint responses. It allows to use different backend, ie: Redis, Memcache, etc. 

The Cache configuration can be set in the `config.py` file.

Extension: <a href="https://github.com/sh4nks/flask-caching" target="_blank">flask-caching</a>

---

## Usage


Assembly exposes `@response.cache` to cache enpoint. The decorator will use request.path by default for the cache_key 

```python
from assembly import Assembly, response, date

class Index(Assembly):

    @response.json
    def index(self):
        return {
            "description": "not cached",
            "date": date.utcnow()
        }

    @response.cache(10)
    @response.json
    def cached(self):
        return {
            "description": "cached",
            "date": date.utcnow()
        }
```

---


## Configuration

Set the configuration below in your `config.py` file.

```python
#--------- CACHING ----------
#: Flask-Cache is used to caching
CACHE = {
    #: CACHE_TYPE
    #: The type of cache to use
    #: null, simple, redis, filesystem,        
    "TYPE": "simple",

    #: CACHE_REDIS_URL
    #: If CHACHE_TYPE is 'redis', set the redis uri
    #: redis://username:password@host:port/db        
    "REDIS_URL": "",

    #: CACHE_DIR
    #: Directory to store cache if CACHE_TYPE is filesystem, it will
    "DIR": ""
}
```

