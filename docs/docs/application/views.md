

## Overview

Assembly views are classes that extend **Assembly** 

By default they are placed in `/views` as modules and may have a template associated to them in the `/templates` folder. 

The can be imported directly in the `__init__.py` or in the `APPS` list in the `wsgi.py` file.

A simple View would with its template would look like this


```
|- views/
    |- __init__.py
    |- main.py
|- templates/
    |- main
        |- Index
            |- index.html
```
 

```python

# views/main.py
from assembly import Assembly

class Index(Assembly):
    def index(self):
        return {
            "name": "Assembly",
            "title": "Assembly For Ever!"
        }

```


```python
# wsgi.py

APPS = {
    "default": [
        "views.main"
    ]
}

```
---

## Working with View

A view is python module (file) that contains classes extending `Assembly`.

Simply create a python file in the `views/` directory, called view module. In the `templates/` create a directory with the same name as the view module. For every class that gets created, have a matching folder name which will contain html files associated to each method names. 

So an action with the following signature `views.admin.Index.index` will have a matching template `templates/admin/Index/index.html`.

If that's too hard to do manually, we can use the generator to help us create a view.

```python
asm gen:view admin
```

### Imports

Turn your classes into Assembly views by extending **Assembly**

```python
from assembly import Assembly

class Index(Assembly):
    def index(self):
        return

```

### Routing

By default Assembly creates routes based on the class name and the method.


### Modifiying routes

Use `@request.route` on classes or method to change the route endpoint

```python
from assembly import Assembly, request

# responds to -> /admin
@request.route("/admin/")
class Index(Assembly):

    # responds to /admin/catalog
    @request.route("catalog")
    def index(self):
        return

```

---

### Routing Rules


#### Index

Class named **Index** or method named **index** will be the root of the endpoint, or the entry point.

```python
# responds to -> /
class Index(Assembly):

    # responds to -> /
    def index(self):
        return
```

#### Class name are base routes

the class name is the base url

```python
# responds to -> /api
class Api(Assembly):

    # responds to -> /api/
    def index(self):
        return 

    # responds to -> /api/items
    def items(self):
        return 

# responds to -> /article/
class Article(Assembly):

    # responds to -> /article/
    def index(self):
        return 

    # responds to -> /article/reviews
    def reviews(self):
        return
```

#### Class name with UpperCamelCase

Class name with UpperCamelCase will turn into dash/hyphen.

```python

# responds to -> /super-hero/
class SuperHero(Assembly):
  def index(self):
    return 

  # responds to -> /super-hero/contact-us/
  def contact_us(self):
    return

```


#### Method names are routes

```python
# responds to -> /
class Index(Assembly):

    # responds to -> /
    def index(self):
        return

    # responds to -> /hello/
    def hello(self):
        return

    # responds to -> /save/
    def save(self):
        return
```

#### Method name with underscore

Methods containing underscore in between, will turn into dash/hyphen

```python
class Index(Assembly):

    # responds to -> /about-us/
    def about_us(self):
        return
```

However, method starting with undescrore are private methods that will not have a route attached them.


```python
class Index(Assembly):

    # will not be assigned a route because it starts with underscore
    def _log_data_info(self):
        return
```

```python

# responds to -> /super-hero/
class SuperHero(Assembly):
    def index(self):
        return 

    # responds to -> /super-hero/contact-us/
    def contact_us(self):
        return

    # will not be assigned a route because it starts with underscore
    def _log_data_info(self):
        return
```


#### RESTful

**get**, **post**, **put**, **delete** will automatically be assigned their method name

```python
class Index(Assembly):

    # will responds on get call
    def get(self):
        return

    # will responds on post call
    def post(self):
        return

    # will responds on delete call
    def delete(self):
        return

    # will responds on put call
    def put(self):
        return

    # will responds on update call
    def update(self):
        return

```


---

## Special methods

Below are methods that are very special to your application

### _before_request

This function will run before each request

```python
class Index(Assembly):

    def _before_request(self, name):
        """
        name: The name of the view that’s about to be called
        """
        pass

    def index(self):
        return

```



### _after_request

This function will run after each request

```python
class Index(Assembly):

    def _after_request(self, name, response):
        """
        name: The name of the view that’s about to be called
        response: The response object. Must return the response
        """
        return response

    def index(self):
        return

```

### _error_handler

This function will catch all HTTPError. 

```python
class Index(Assembly):

    def _error_handler(self, error):
        return {
            "e": error
        }

```

### _error\_$errorCode

This function will catch an HTTP Error Code

```python
class Index(Assembly):

    # will catch 404 only
    def _error_404(self, error):
        return {
            "e": error
        }

    # will catch 401 only
    def _error_401(self, error):
        return {
            "e": error
        }

    # will catch 500 only
    def _error_500(self, error):
        return {
            "e": error
        }

```


### _before\_$methodName

This function will run before each time $methodName is called

```python
class Index(Assembly):

    def _before_about_us(self, name):
        """
        name: The name of the view that’s about to be called
        """
        pass

    def about_us(self):
        pass

```


### _after\_$methodName

This function will run after each time $methodName is called

```python
class Index(Assembly):

    def _after_about_us(self, name):
        """
        name: The name of the view that’s about to be called
        response: The response object. Must return the response
        """
        return response

    def about_us(self):
        pass

```

---


## Request

Request is a Proxy to Flask request with extra functionalities. For example it adds route decorator, cors decorator, etc.  

```python
from assembly import request
```

Go to: **[Request](../advanced/request.md) **

---

## Response

By default, Assembly will attempt to match a template with the view. Sometimes you may want to return JSON or cache the response. The `response` module provides some decorators to help with some response functionalities.

```python
from assembly import response
```

Go to: **[Response](../advanced/response.md) **

---

## Redirect

Redirect helps you redirect to different enpoint using the method name via 'self' or the class itself. Assembly knows what to do. also allows inter within

```python
from assembly import redirect
```

Go to: **[Redirect](../advanced/redirect.md) **

---

## url_for

Generates a URL to the given endpoint with the method provided. It's a proxy to Flask url_for, but add some functionalities.

Extra arguments will be used as query params. To get the full url, add `_external=True`.

```python
from assembly import Assembly, url_for, views


class Index(Assembly):

    def index(self):
        return {
            "about-us-url": url_for(self.about_us),
            "blog-url": url_for(Blog.index),
            "articles-url": url_for(views.views.articles.Articles.index),
        }

    def about_us(self):
        return

class Blog(Assembly):
    def index(self):
        return


# views/articles.py

class Articles(Assembly):

    def index(self):
        return 


```

---

## Models

Models can be used easily by importing the `models` object. It contains a reference of every models that have been created with `db.Model`

Learn more on **[Models](../application/models.md) **


```python
# views/models.py

from assembly import db

class Article(db.Model):
    title = db.Column(db.String(250))
    content = db.Column(db.Text)

class Author(db.Model):
    name = db.Column(db.String(250))    

```


```python

from assembly import Assembly, models

class Index(Assembly):

    def articles(self):
        articles = models.Article.query()
        articles = articles.paginate(page=1, per_page=20)
        return {
            "articles": articles
        }

```

---

## Config

You can access config variable in your view by using `config`. `config` is a dict to retrieve any info. It also allows dot notation to drill down property

Go to: **[Config](../config.md) **



```python

from assembly import Assembly, config

class Index(Assembly):

    def index(self):
        app_version = config.get("APPLICATION_VERSION")
        default_date = config.get("DATE_FORMAT.default")
        return

```

---

## Error Handling

A special method _error_handler can be added in your view class to capture any HTTPException.

```python
from assembly import HTTPError
```

Go to: **[Error Handling](../advanced/error-handling.md) **

---

## Working with dates

To work with dates, Assembly provides `date`.

```python
from assembly import date
```

Go to: **[Dates](../advanced/date.md) **

---


## Session

Working with session

```python
from assembly import session
```

Go to: **[Session](../advanced/sessions.md) **

---
## Flash

Working with flash

```python
from assembly import flash
```

Go to: **[Flash](../advanced/flash.md) **

---
## Form Validations

Working with form validations

```python
from assembly import forms
```

Go to: **[Form Validations](../advanced/form-validations.md) **


---
## Login Manager

Login Manager

```python
from assembly import login_manager
```

Go to: **[Form Validations](../advanced/login-manager.md) **
