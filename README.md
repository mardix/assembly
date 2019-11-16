# Assembly

### A Pythonic Object-Oriented Web Framework built on Flask

--- 

**Assembly** is a pythonic object-oriented, mid stack, batteries included framework built on Flask, that adds structure 
to your Flask application, and group your routes by class.

**Assembly** allows developers to build web applications in much the same way they would build any other object-oriented Python program. 

Technically **Assembly** is an attempt of making a simple framework based on Flask Great Again!

---

[Documentation](https://mardix.github.io/assembly)

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

- Smart template: automatically map the class and method name, to folder and html file

- Auto rendering by returning a dict of None

- Markdown ready: Along with  HTML, it can also properly parse Markdown

- Auto route can be edited with @request.route()

- Restful: GET, POST, PUT, DELETE

- REST API Ready

- bcrypt is chosen as the password hasher

- Simplified error handling

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- ORM: [Active-Alchemy](https://github.com/mardix/active-alchemy) (SQLALchemy wrapper)

- Dates: Uses Arrow for dates 

- Active-Alchemy saves the datetime as arrow object, utc_now

- CSRF on all POST

- Storage: Local, S3, Google Storage [Flask-Cloudy](https://github.com/mardix/flask-cloudy)

- Email: SMTP, SES

- Caching

- CORS


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
      {% block content %}{% endblock %}
    </div>
  </body>
</html>

```

#### 4.1  Edit Index/index.html
```

<!-- main/templates/Index/index.html -->

{% extends 'main/layouts/base.html' %}

{% block title %}Welcome to my Assembly Site {% endblock %}

{% block content %}
    <div>
        <h1>{{ title }}</h1>
    </div>
    <div>
        {{ content }}
    </div>
{% endblock %}


```


#### Serve your first application

If everything is all set, all you need to do now is run your site:

```
asm-admin serve
```

It will start serving your application by default at `127.0.0.1:5000`

Go to http://127.0.0.1:5000/ 

---

I hope this wasn't too bad. Now Read The Docs at [http://mardix.github.io/assembly/](http://mardix.github.io/assembly/)
for more 

Thanks, 

Mardix :) 

--- 

## Read The Docs

To dive into the documentation, Read the docs @ [http://mardix.github.io/assembly/](http://mardix.github.io/assembly/)

---

License MIT

Copyright: 2019 - Forever Mardix

