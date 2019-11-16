


<div style="text-align:center; margin-bottom: 60px;">
<h1 style="font-size: 3.5em; font-weight: bold;  color: #7c4dff">
    <i class="md-icon">local_florist</i>
    Assembly
    <i class="md-icon">local_florist</i>
</h1>
<p></p>
<h2 style="">A Pythonic Object-Oriented Web Framework built on Flask</h2>
</div>


<div style="text-align:center"><img src="/img/assembly.png"></div>

---

## <div style="text-align:center">About</div>

**Assembly** is a pythonic object-oriented, mid stack, batteries included framework built on Flask, that adds structure 
to your Flask application, and group your routes by class.

**Assembly** allows developers to build web applications in much the same way they would build any other object-oriented Python program. 

Technically **Assembly** is an attempt of making a simple framework based on Flask Great Again!


**[Installation Guide](install.md) **

---

## <div style="text-align:center">Quick Start</div>

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


## Features List

- Smart routing: automatically generates routes based on the classes and methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at '/user-account'

- Class methods (action) could be accessed: hello_world(self) becomes 'hello-world'

- Easy rending and render decorator

- Auto route can be edited with @route()

- Restful: GET, POST, PUT, DELETE

- REST API Ready

- Markdown friendly. Inclusion of a markdown file will turn into HTML

- BCRYPT is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- Database/ORM: [Active-Alchemy](https://github.com/mardix/active-alchemy) (SQLALchemy wrapper)

- CSRF on all POST

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

- Local server

---

Credits: Flask, Flask-Classy