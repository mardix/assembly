


<div style="text-align:center; margin-bottom: 60px;">
<h1 style="font-size: 3.5em; font-weight: bold;  color: #7c4dff">
    <i class="md-icon">local_florist</i>
    Assembly
    <i class="md-icon">local_florist</i>
</h1>
<p></p>
<h2 style="">A Pythonic Object-Oriented Web Framework built on Flask</h2>
</div>


<div style="text-align:center"><img src="./img/assembly.png"></div>

---

## About

**Assembly** is a pythonic object-oriented, mid stack, batteries included framework built on Flask, that adds structure to your Flask application, and group your routes by class.

**Assembly** allows you to build web applications in much the same way you would build any other object-oriented Python program. 

**Assembly** helps you create small to enterprise level applications easily.

**Assembly** Makes Flask Great Again!


**[Installation Guide](install.md) **

---

## Why Assembly ?

Flask is very easy and simple. It's fun to put a few endpoints in a single file. However when your application starts growing into an endless of endpoints, tons of models and views, or your team is having more people, it is very necessary to have some sort of structure in your application. 

And that's what Assembly does. Assembly adds structure to Flask application. Assembly removes a lot of Flask boilerplate. Assembly makes your Flask application scalable and easy to work with.

Instead of having loose endpoints per functions, Assembly organizes all groups of endpoints per class. Instead of each time rendering the template for each endpoint manually, Assembly matches the name of the method of the class, to the name of the template file, making it a one-one match. 

Assembly automatically loads your models and configuration. 

Assembly is very extensible, as every View is it's own package. Making it easy to add and remove.

**Assembly** Makes Flask Great Again!

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

    |- _data/
```



### 3. Edit your first view

```

# main/__init__.py

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


## Features List

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

Image Credit - License: Non-commercial Use : https://imgbin.com/png/q2HLy9Kx/flower-watercolor-painting-png 
