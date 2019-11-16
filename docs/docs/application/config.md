
Path: `./__config__.py`.

```
from assembly import config 
```

---

Assembly uses class-based configuration, and the config will be loaded upon startup.

    class BaseConfig(object):

        APPLICATION_NAME = "Assembly"

        APPLICATION_URL = ""

        APPLICATION_VERSION = "0.0.1"

        GOOGLE_ANALYTICS_ID = ""

        ADMIN_EMAIL = None

        CONTACT_EMAIL = None

        PAGINATION_PER_PAGE = 20

        ...


    class Development(BaseConfig):
        """
        Config for development environment
        """
        SERVER_NAME = None
        DEBUG = True
        SECRET_KEY = "PLEASE CHANGE ME"


    class Production(BaseConfig):
        """
        Config for Production environment
        """
        SERVER_NAME = "abc.com"
        DEBUG = False
        SECRET_KEY = "My Prod Secret"
        COMPRESS_HTML = True


It is recommended to have a base class, `BaseConfig`, and your environment classes `Development`, `Production` which are subclasses
of the `BaseConfig`, this way they can share some common config.

The environment classes will be loaded on Assembly startup. By default, and in development, Assembly will attempt to load the `Development` if one isn't provided.

To switch to a different config, you have to set the environment variable, or in production

```
export ASSEMBLY_ENV=Production
export ASSEMBLY_PROJECT=default
```

or to set the application along with the environment

```
ASSEMBLY_ENV=Production ASSEMBLY_PROJECT=default asm-admin serve
```

The code above will load the `Production` config.

One main advantage of having your config like that, is that you have the ability of using different config for different
environment, could be for testing, prod, dev, etc.

---
