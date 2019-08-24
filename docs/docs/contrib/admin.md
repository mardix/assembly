
Mocha makes it easy to turn your view classes into Admin area with restricted access.

It automatically setup the minimum permission, the layouts an everything.

This is simple accomplished by decorating your admin classes with `@contrib.admin`

### Example

    import mocha.contrib

    @mocha.contrib.admin
    class Admin(Mocha):

        def index(self):
            pass

        def hello(self):
            pass

## Config
