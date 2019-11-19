# Assembly

### A Pythonic Object-Oriented Web Framework built on Flask

--- 

**Assembly** is a pythonic object-oriented, mid stack, batteries included framework built on Flask, that adds structure to your Flask application, and group your routes by class.

**Assembly** allows you to build web applications in much the same way you would build any other object-oriented Python program. 

**Assembly** helps you create small to enterprise level applications easily.

**Assembly** Makes Flask Great Again!

--- 

### [Assembly Documentation](http://mardix.github.io/assembly/)

Assembly Version: 1.x.x

---

## Assembly in action 


```
# views.py

from assembly import (Assembly, response, request, HTTPError)

# Extends to Assembly makes it a route automatically
# By default, Index will be the root url
class Index(Assembly):

    # index is the entry route
    # -> /
    index(self):
        return "welcome to my site"

    # method name becomes the route
    # -> /hello/
    hello(self):
        return "I am a string"

    # undescore method name will be dasherize
    # -> /about-us/
    about_us(self):
        return "I am a string"


# The class name is part of the url prefix
# This will become -> /blog
class Blog(Assembly):
    
    # index will be the root 
    # -> /blog/
    index(self):
        return [
            {
                "title": "title 1",
                "content": "content"
            },
            ...
        ]

    # with params. The order will be respected
    # -> /comments/1234/
    # 1234 will be passed to the id
    comments(self, id):
        return [
            {
                comments...
            }
        ]


# It's also Restful
class Api(Assembly):

    # method named get, automatically accepts get method
    # -> GET /api/
    get(self):
        return {
            "message": "This will show on get call"
        }

    # method named post, automatically accepts post method
    # -> POST /api/
    post(self):
        return {
            "message": "This will show on POST call"
        }

    # Can change the response to json
    # -> /api/about/
    @response.json
    about(self): 
        return {
            "name": "Assembly",
            "version": "1.0.1"
        }

    # endpoint with different method 
    # -> POST /api/submit/
    @request.post
    submit(self):
        return {
            "message": "This will show on POST call only"
        }

    # This will throw an Unauthorize error
    error(self):
        raise HTTPError.Unauthorized()

```


---

## Decisions made for you + Features

- Smart routing: automatically generates routes based on the classes and methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at '/user-account'

- Class methods (action) could be accessed: hello_world(self) becomes 'hello-world'

- RESTful API

- Automatic view rendering

- Auto route can be edited with @route()

- Markdown friendly. Inclusion of a markdown file will turn into HTML

- BCRYPT is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- Database/ORM: [Active-Alchemy](https://github.com/mardix/active-alchemy) (SQLALchemy wrapper)

- CSRF on all POST

- Idiomatic HTTP error responses

- Storage: Local, S3, Google Storage [Flask-Cloudy](https://github.com/mardix/flask-cloudy)

- Mailer (SES or SMTP)

- Arrow for date and time

- Caching

- JWT

- Pagination

- Signals: to dispatch messages and data to other part of the application

- Markdown

- Jinja2 for templating language

- Multi application

- Web Assets

- CLI

- Inbuilt development server


---

## Quickstart

This quickstart will allow us to go with Assembly from 0 to 100!

### 1. Install Assembly

Install Assembly with `pip install assembly`

It is highly recommended to use a virtualenv, in this case let's
use VirtualenvWrapper (you can use any that is convenient for you)

```
mkvirtualenv my-first-app

workon my-first-app

pip install assembly

```


### 2. Initialize your application

Initialize Assembly with `asm-admin init`

CD into the folder you intend to create the application, then run `asm-admin init`. 
This will setup the structure along with the necessary files to get started

```

cd app-dir

asm-admin init

```

Upon initialization you should have a structure similar to this:

```
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- main
        |- __init__.py
        |- __models__.py
        |- templates
            |- Index
                |- index.html
            |- layouts
                |- base.html
        |- static
        |- cli.py

    |- __data__/
```



### 3. Edit your first view

```

# main/__init__.py

from assembly import (Assembly, response)

class Index(Assembly):
    
    index(self):
        return {
            "title": "Assembly is awesome",
            "content": "That is a true fact"
        }

    @response.json
    api(self):
        return {
            "name": "Assembly",
            "version": "x-to-infinity"
        }

```

### 4. Edit your template

#### 4.0 Edit base layout 

```
<!-- main/templates/layouts/base.html -->

<!doctype html>
<html lang="en">
  <head>
    <title>{% block title %}{% endblock %}</title>
  </head>

  <body>
    <div class="container">
      {% block body %}{% endblock %}
    </div>
  </body>
</html>

```

#### 4.1  Edit Index/index.html
```

<!-- main/templates/Index/index.html -->

{% extends 'main/layouts/base.html' %}

{% block title %}Welcome to my Assembly Site {% endblock %}

{% block body %}
    <div>
        <h1>{{ title }}</h1>
    </div>
    <div>
        {{ content }}
    </div>
{% endblock %}


```


### 5. Serve your first application

If everything is all set, all you need to do now is run your site:

```
asm-admin serve
```

It will start serving your application by default at `127.0.0.1:5000`

Two endpoints will be available:

- `http://127.0.0.1:5000/` which will show an HTML
- `http://127.0.0.1:5000/api/` which will a json response


--- 

### Learn More: [Assembly Documentation](http://mardix.github.io/assembly/)

---

License MIT

Copyright: 2020 - Forever Mardix

