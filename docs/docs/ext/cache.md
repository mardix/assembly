`flask_cache` is used to cache data. It allows to use different backend, ie: Redis, Memcache, etc.


#### Import

    from mocha import cache


#### Decorator

    from mocha import Mocha, cache

    class Index(Mocha):

        @cache.cached(3600)
        def index(self):
            return {

            }


#### Config

    #: CACHE_TYPE
    #: The type of cache to use
    #: null, simple, redis, filesystem,
    CACHE_TYPE = "simple"

    #: CACHE_REDIS_URL
    #: If CHACHE_TYPE is 'redis', set the redis uri
    #: redis://username:password@host:port/db
    CACHE_REDIS_URL = ""

    #: CACHE_DIR
    #: Directory to store cache if CACHE_TYPE is filesystem, it will
    CACHE_DIR = ""


Extension: [flask-cache](https://github.com/sh4nks/flask-caching)
