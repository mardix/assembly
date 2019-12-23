
## Overview

Redirect is a Proxy to Flask redirct. Redirect helps you redirect to different enpoint using the method name via 'self' or the class itself. Assembly knows what to do. also allows inter within

## Usage


```python
from assembly import Assembly, redirect

class Index(Assembly):

    def about_us(self):
        return "This is about us"

    # redirect to 'about_us' method
    # redirect by providing the method name with 'self'
    def redirect_me(self):
        return redirect(self.about_us)
```

### Redirect by Class name

```python
from assembly import Assembly, redirect

class Index(Assembly):

    # redirects a diffrent class, no need to know the endpoint
    def redirect_me(self):
        return redirect(Blog.all_posts)

class Blog(Assembly):
    def all_posts(self):
        return

```

### Redirect with other Views

For View classes that are not in the same file, you can redirect by using the `views` object, which contains the reference of every view modules.

```python
# views/main.py

from assembly import Assembly, redirect, views

class Index(Assembly):

    # redirects a different class, no need to know the endpoint
    def redirect_me(self):
        return redirect(views.views.admin.Index.login)


```

```python
# views/admin.py

from assembly import Assembly, request

@request.route("/admin/")
class Index(Assembly):

    def login(self):
        return

```

