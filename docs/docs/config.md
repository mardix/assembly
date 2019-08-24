
Location: `/application/config.py`.

---

Mocha uses class-based configuration, and the config will be loaded upon startup.

    class BaseConfig(object):
        """
        Base Configuration.
        """

        APPLICATION_NAME = "Mocha"

        APPLICATION_URL = ""

        APPLICATION_VERSION = "0.0.1"

        GOOGLE_ANALYTICS_ID = ""

        ADMIN_EMAIL = None

        CONTACT_EMAIL = None

        PAGINATION_PER_PAGE = 20

        ...


    class Dev(BaseConfig):
        """
        Config for development environment
        """
        SERVER_NAME = None
        DEBUG = True
        SECRET_KEY = "PLEASE CHANGE ME"


    class Prod(BaseConfig):
        """
        Config for Production environment
        """
        SERVER_NAME = "abc.com"
        DEBUG = False
        SECRET_KEY = "My Prod Secret"
        COMPRESS_HTML = True


It is recommended to have a base class, `BaseConfig`, and your environment classes `Dev`, `Prod` which are subclasses
of the `BaseConfig`, this way they can share some common config.

The environment classes will be loaded on Mocha startup. By default, and in development, Mocha will attempt to load
 the `Dev` if one isn't provided.

To switch to a different config, you have to set the environment variable

    env=prod mocha :serve

or to set the application along with the environment

    app=main:prod mocha :serve

The code above will load the `Prod` config.

One main advantage of having your config like that, is that you have the ability of using different config for different
environment, could be for testing, prod, dev, etc.

---
