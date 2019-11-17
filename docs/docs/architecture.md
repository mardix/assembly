
## Overview

Assembly tries to keep it simple by providing a flat structure for your application and gives you 
the freedom to do whatever else. 

It lays out a basic layout, so the application can be consistent. 

---

## Structure

A basic application structure looks like this

```
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- app.json
    |- __data__  
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

```

---

### Base files

Base files are at the root of the application. And `wsgi.py`, `config.py` are required by Assembly.


```
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- app.json
    |- __data__  
```

- `wsgi.py` is the application object. (required)

- `config.py`: contains class based configurations (required)

- `requirements.txt`: contains application dependencies including `assembly`

- `app.json`: Application manifest to deploy using Gokku

- `__data__`: A variable directory, to put misc files, uploads, etc.


---

### View Package Structure

View Package are simply a package/directory that contains at least `__init__.py` and can be imported into the `APPS` list in the `wsgi.py` file. 

Additionally, you can find `__models__.py`, `templates/`, `static/`

The view name is the folder. The example below show the `main` view.

```
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

```

- `main` view directory
- `__init__.py` contains all the View classes
- `__models__.py` contains all the Models for that View
- `templates` contains templates for the each endpoint in the View classes
- `static` contain the static files, images, css, js, etc.
- `cli.py` Custom CLI for that view.

`__init__.py`, `__models__.py`, `templates/`, `static/` will be loaded implicitely by Assemby. Only `__init__.py` is required.

`__init__.py` is also served as files containing all the view classes.

---

## View Class structure

You can place your view classes in `__init__.py`. Assembly will automatically load them when they are added in the APPS list.

Aside from importing the `assembly` package, nothing special needs to be done in the View. Just work on your application like you would in your normal Python file. As a matter of fact this is a normal Python file.

```
# main/__init__

from assembly import Assembly

class Index(Assembly):
  def index(self):
    return

```

---

### Multiple Classes

It's ok to have multiple classes in your View. They will be treated properly with the proper endpoint.

```

# main/__init__

from assembly import Assembly, request

# responds to /
class Index(Assembly):
  index(self):
    return 

# responds to /api/
class Api(Assembly):
  index(self):
    return


# responds to /admin/
class Admin(Assembly):
  index(self):
    return

```

---

### Namespace

Everything is properly namespaced, however the only time you may have some clashes is when more than one class has the same class name. To fix that, just use a different route name for the class base.

```
# main/__init__

from assembly import Assembly

# responds to /
class Index(Assembly):
  index(self):
    return 

---

# admin/__init__

from assembly import Assembly, request

# responds to /admin/
@request.route("/admin/")
class Index(Assembly):
  index(self):
    return 
```


## View Templates

Assembly uses Jinja as templating language. 

Templates are mapped by their class and method name

Having a sctructure like this...

```
|- admin
    |- __init__.py
    |- __models__.py
    |- templates
        |- Index
            |- index.html
            |- login.html
        |- Articles
            |- index.html
            |- all.html
    |- static
    |- cli.py

```

our View class will have 


```
# admin/__init__.py

from assembly import Assembly

class Index(Assembly):
  def index(self):
    return 

  def login(self):
    return

class Articles(Assembly):
  def index(self):
    return 

  def all(self):
    return

```

--

## View Static

Assembly uses Flask-Assets to help manage static assets, ie: images, js, css in your application

