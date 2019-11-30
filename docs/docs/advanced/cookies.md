## Overview

Assembly allows you to easily, set, get and delete cookie. It exposes some functions
to help you with that.

*version: 1.1.0*

---

## Usage

### Import

```python
from assembly import  set_cookie, get_cookie, delete_cookie
```

---

### set_cookie

To set a cookie

```python
from assembly import (Assembly, set_cookie)

class Index(Assembly):

  def index(self):

    set_cookie("my_key", "my_value")

    return 

```

```python
set_cookie(
          key,
          value="",
          max_age=None,
          expires=None,
          path="/",
          domain=None,
          secure=False,
          httponly=False,
          samesite=None)

Sets a cookie. The parameters are the same as in the cookie `Morsel`
object in the Python standard library but it accepts unicode data, too.

:param key: the key (name) of the cookie to be set.
:param value: the value of the cookie.
:param max_age: should be a number of seconds, or `None` (default) if
                the cookie should last only as long as the client's
                browser session.
:param expires: should be a `datetime` object or UNIX timestamp.
:param path: limits the cookie to a given path, per default it will
              span the whole domain.
:param domain: if you want to set a cross-domain cookie.  For example,
                ``domain=".example.com"`` will set a cookie that is
                readable by the domain ``www.example.com``,
                ``foo.example.com`` etc.  Otherwise, a cookie will only
                be readable by the domain that set it.
:param secure: If `True`, the cookie will only be available via HTTPS
:param httponly: disallow JavaScript to access the cookie.  This is an
                  extension to the cookie standard and probably not
                  supported by all browsers.
:param samesite: Limits the scope of the cookie such that it will only
                  be attached to requests if those requests are
                  "same-site".

```

---

### get_cookie

To retrieve a cookie. It will return `None` if the key doesn't exist.

You can also retrieve the cookie with `request.cookies`

```python
from assembly import (Assembly, get_cookie)

class Index(Assembly):

  def index(self):

    get_cookie("my_key")

    return 

```

---

### delete_cookie

To delete a cookie that was set. It will silently fail if it doesn't exist

```python
from assembly import (Assembly, delete_cookie)

class Index(Assembly):

  def index(self):

    delete_cookie("my_key")

    return 

```


```python
delete_cookie(self, key, path="/", domain=None)

Delete a cookie.  Fails silently if key doesn't exist.
:param key: the key (name) of the cookie to be deleted.
:param path: if the cookie that should be deleted was limited to a
              path, the path has to be defined here.
:param domain: if the cookie that should be deleted was limited to a
                domain, that domain has to be defined here.
        
```

