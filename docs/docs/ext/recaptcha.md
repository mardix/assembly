

Recaptcha implements the Google recaptcha in your application.

#### Import

    from mocha import recaptcha


#### Implement in Jinja

To include the recaptcha in your template add the code below

    {{ recaptcha }}


#### Verify code


    class Index(Mocha):

        def send_data(self):
            if recaptcha.verify():
                # everythings is ok
            else:
                # FAILED


#### Config

    #: Flask-Recaptcha
    #: Register your application at https://www.google.com/recaptcha/admin

    #: RECAPTCHA_ENABLED
    RECAPTCHA_ENABLED = True

    #: RECAPTCHA_SITE_KEY
    RECAPTCHA_SITE_KEY = ""

    #: RECAPTCHA_SECRET_KEY
    RECAPTCHA_SECRET_KEY = ""


Extension: [flask-recaptcha](https://github.com/mardix/flask-recaptcha)

To register your application go [https://www.google.com/recaptcha/admin](https://www.google.com/recaptcha/admin)
