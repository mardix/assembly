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

### Pythonic Routes

Routes are created based on the class and the method names by default. 
Class named *Index* and method named *index* will be the entry point of the route.


```python
from assembly import Assembly

# Extends to Assembly makes it a route automatically
# By default, Index will be the root url
class Index(Assembly):

    # index is the entry route
    # -> /
    def index(self):
        return "welcome to my site"

    # method name becomes the route
    # -> /hello/
    def hello(self):
        return "I am a string"

    # undescore method name will be dasherize
    # -> /about-us/
    def about_us(self):
        return "I am a string"

# The class name is part of the url prefix
# This will become -> /blog
class Blog(Assembly):

    # index will be the root
    # -> /blog/
    def index(self):
        return [
            {
                "title": "title 1",
                "content": "content"
            },
        ]

    # with params. The order will be respected
    # -> /blog/comments/1234/
    # 1234 will be passed to the id
    def comments(self, id):
        return [
            {
                # comments
            }
        ]

```

### RESTful

Methods named **get**, **post**, **put**, **delete**, **update** will automatically accept the associated methods GET, POST, PUT, DELETE UPDATE respectively.

But you can also assign a different method by using the appropriate request decorator.


```python
from assembly import Assembly, request

class Api(Assembly):

    # method named get, automatically accepts get method
    # -> GET /api/<id>
    def get(self, id):
        return {
            "message": "This will show on get call"
        }

    # method named post, automatically accepts post method
    # -> POST /api/
    def post(self):
        return {
            "message": "This will show on POST call"
        }
        
    # Example of a different route assigned a method
    # /submit/ will only accept POST call
    # -> POST /submit/
    @request.post
    def submit(self):
        return "Submitted!"
```

### Multi Response Type

By default Assembly will map the route to its associated template. It's very convenient as you don't have to explicitely render the template.

But you can also make the route return JSON.


```python
# views/main.py

from assembly import (Assembly, response, request, HTTPError)

# Extends to Assembly makes it a route automatically
# By default, Index will be the root url
class Index(Assembly):

    # index is the entry route
    # -> /
    # it will render its associated template from 
    # 'templates/main/Index/index.html'
    def index(self):
        return 

    # returning string will be rendered as string.
    # -> /hello/
    def hello(self):
        return "I am a string"

    # returns a json response
    # -> /api/
    @response.json
    def api(self):
        return {
            "name": "Assembly",
            "title": "Assembly for ever",
            "items": [
                # list of items
            ]
        }

    # This will throw an Unauthorize error
    def error(self):
        raise HTTPError.Unauthorized()

```

---

## Decisions made for you + Features

- Smart Pythonic Routing: automatically generates routes based on the classes and methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at '/user-account'

- Class methods (action) could be accessed: hello_world(self) becomes 'hello-world'

- RESTful: good to create API endpoints, which can also return JSON object

- Automatic view rendering

- Auto route can be edited with @request.route()

- Multi responses type: HTML, JSON, Text 

- Markdown friendly: Inclusion of a markdown file will turn into HTML

- BCRYPT is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- Database/ORM: SQLAlchemy base to work DB models via [Active-Alchemy](https://github.com/mardix/active-alchemy)

- Login Manager: for user session management via Flask-Login

- Form Validations: Validate your forms via WTForms

- CSRF on all POST: to protect against CSRF attacks 

- Idiomatic HTTP error responses

- Storage: to access and store files from  Local, S3, Google Storage with [Flask-Cloudy](https://github.com/mardix/flask-cloudy)

- Mailer: To send email using SMTP or AWS SES

- Arrow: Human friendly date and time library

- CLI/Scripts: Create your own scripts to be used on the command line.

- Caching: To cache responses

- JWT

- Pagination

- Signals: to dispatch messages and data to other part of the application

- Markdown

- Jinja2 for templating language

- Multi application: Allow to share the same codebase but with multiple applications.

- Web Assets: To easily manage your static content: css, js, images etc...

- Inbuilt development server

- And much more...

---

## Quick Start

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

Initialize Assembly with `asm gen:init`

CD into the folder you intend to create the application, then run `asm gen:init`.
This will setup the structure along with the necessary files to get started

```
cd app-dir

asm gen:init

```

Upon initialization you should have a structure similar to this:

```
-- /
    |- wsgi.py
    |- requirements.txt
    |- lib/
        |- config.py
        |- models.py
    |- run
        |- scripts.py
    |- views/
        |- main.py
    |- templates/
        |- layouts/
            |- base.html    
        |- main/
            |- Index/
                |- index.html
    |- static/
    |- data/
```

### 3. Edit your first view

```python

# views/main.py

from assembly import (Assembly, response)

class Index(Assembly):

    def index(self):
        return {
            "title": "Assembly is awesome",
            "content": "That is a true fact"
        }

    @response.json
    def api(self):
        return {
            "name": "Assembly",
            "version": "x-to-infinity"
        }

```

### 4. Edit your template

#### 4.0 Edit base layout

```html
<!-- templates/layouts/base.html -->

<!DOCTYPE html>
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

#### 4.1 Edit Index/index.html

```html
<!-- templates/main/Index/index.html -->

{% extends 'layouts/base.html' %} {% block title %}Welcome to my Assembly Site {% endblock %} {% block body %}
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

```sh
asm gen:serve
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
