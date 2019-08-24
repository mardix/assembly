

**csrf** prevents cross-site request forgery (CSRF) on your application

#### Import

    from mocha import csrf


Automatically all POST, UPDATE methods will require a CSRF token, unless explicitly exempt.

To exempt and endpoint, jus add the decorator `csrf.exempt`

    class Index(Mocha):

        def index(self):
            pass

        @csrf.exempt
        def exempted_post(self):
            pass

        @post()
        def save_data(self):
            pass

In the example above, when posting to `/exempted-post/` it will not require the CSRF token,
however `/save-data/` requires it.



#### Config

        CSRF_COOKIE_NAME  # _csrf_token
        CSRF_HEADER_NAME  # X-CSRFToken
        CSRF_DISABLE
        CSRF_COOKIE_TIMEOUT
        CSRF_COOKIE_SECURE
        CSRF_COOKIE_HTTPONLY
        CSRF_COOKIE_DOMAIN
        CSRF_CHECK_REFERER
        SEASURF_INCLUDE_OR_EXEMPT_VIEWS


**About**

Extension: [flask-seasurf](https://github.com/maxcountryman/flask-seasurf)

SeaSurf is a Flask extension for preventing cross-site request forgery (CSRF).

CSRF vulnerabilities have been found in large and popular sites such as YouTube.
These attacks are problematic because the mechanism they use is relatively easy to exploit.
This extension attempts to aid you in securing your application from such attacks.

