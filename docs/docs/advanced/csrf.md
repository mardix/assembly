

## Overview

Assembly uses **flask-seasurf** to prevent cross-site request forgery (CSRF)

Extension: <a href="https://github.com/maxcountryman/flask-seasurf" target="_blank">flask-seasurf</a>


---

## Usage

**Automatically all POST, UPDATE methods will require a CSRF token, unless explicitly exempt**. (That's a good thing)

This includes POST from FORMS or AJAX calls.

---

### Validate CSRF

To validate CSRF, use `request.csrf`.

If CSRF fails to validate, it will throw a **Forbidden/403** error.

```
from assembly import Assembly, request

class Index(Assembly):

    def post(self):
        if request.csrf.validate():
            # everything is good here
            pass

```
---

### Exempt CSRF

Assembly exposes `@request.csrf.exempt` to exclude a view from CSRF validation.

```
from assembly import Assembly, request

class Index(Assembly):

    def post(self):
        # this will require csrf

    @request.post
    @request.csrf.exempt
    def exempt_this(self):
        # this will not require CSFR


```

In the example above, when POSTing to /post/ it will require the CSRF token, however POSTing to /exempt-this/ will not requires it.


---

## Configuration

Set the configuration below in your `config.py` file.

```
    CSRF_COOKIE_NAME="_csrf_token"
    CSRF_HEADER_NAME="X-CSRFToken"
    CSRF_DISABLE
    CSRF_COOKIE_TIMEOUT
    CSRF_COOKIE_SECURE
    CSRF_COOKIE_HTTPONLY
    CSRF_COOKIE_DOMAIN
    CSRF_CHECK_REFERER
    SEASURF_INCLUDE_OR_EXEMPT_VIEWS
```



