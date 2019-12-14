
## Overview

Assembly tries to keep it simple by providing a flat structure for your application and gives you 
the freedom to do whatever else. 

It lays out a basic layout, so the application can be consistent. 

---

## Structure

A basic application structure looks like this

```sh
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- data/
    |- modules/ 
      |- main
          |- __init__.py
          |- __views__.py
          |- __models__.py
          |- templates
              |- Index
                  |- index.html
              |- layouts
                  |- base.html
          |- static
          |- scripts.py

```

---

### Base files

Base files are at the root of the application. And `wsgi.py`, `config.py` are required by Assembly.


```sh
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- modules/
    |- data/  
```

- `wsgi.py` is the application object. (required)

- `config.py`: contains class based configurations (required)

- `requirements.txt`: contains application dependencies including `assembly` (required)

- `modules`: a directory containing the view modules

- `data`: a directory containing the various data, uploads, etc.


---

### View Module Structure

View Module are simply a package/directory that contains a `__views__.py` and can be imported into the `APPS` list in the `wsgi.py` file. 

By default the view modules will be placed under `/modules/`.

Additionally, it may contain `__models__.py`, `templates/`, `static/`

The view name is the folder. The example below show the `main` view.

```sh
|- main
    |- __views__.py
    |- __models__.py
    |- templates
        |- Index
            |- index.html
        |- layouts
            |- base.html
    |- static
    |- scripts.py

```

- `main` view module directory
- `__init__.py` the init file
- `__views__.py` contains all the View classes
- `__models__.py` contains all the Models for that View
- `templates` contains templates for the each endpoint in the View classes
- `static` contain the static files, images, css, js, etc.
- `scripts.py` Custom scripts for that view.

`__views__.py`, `__models__.py`, `templates/`, `static/` will be loaded implicitely by Assemby.

---

## View Class structure

By convention, it is recommended to have your view classes in `__views__.py`. Assembly will automatically load them when they are added in the APPS list.

Aside from importing the `assembly` package, nothing special needs to be done in the View. Just work on your application like you would in your normal Python file. As a matter of fact this is a normal Python file.

```python
# modules/main/__views__.py

from assembly import Assembly

class Index(Assembly):
  def index(self):
    return

```

---

### Multiple Classes

It's ok to have multiple classes in a single view file, `__views__.py`. They will be treated properly with the proper endpoint.

```python

# modules/main/__views__.py

from assembly import Assembly, request

# responds to /
class Index(Assembly):
  def index(self):
    return 

# responds to /api/
class Api(Assembly):
  def index(self):
    return


# responds to /admin/
class Admin(Assembly):
  def index(self):
    return

```

---

### Namespace

Everything is properly namespaced, however the only time you may see some clashes is when more than one class has the same class name. To fix that, just use a different **route endpoint** for the class.

```python
# modules/main/__views__.py

from assembly import Assembly

# responds to /
class Index(Assembly):
  def index(self):
    return 

---

# modules/admin/__views__.py

from assembly import Assembly, request

# responds to /admin/
@request.route("/admin/")
class Index(Assembly):
  def index(self):
    return 

```

---

## View Templates

Assembly uses Jinja as templating language. 

Templates are mapped by their class and method name in the view.

Having a View like this...

```python
# modules/admin/__views__.py

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


class Movies(Assembly):
  def index(self):
    return 

  def guide(self):
    return

  def channels(self):
    return



```

will map to templates below

```
|- admin
    |- __views__.py
    |- __models__.py
    |- templates
        |- Index
            |- index.html
            |- login.html
        |- Articles
            |- index.html
            |- all.html
        |- Movies
            |- index.html
            |- guide.html            
            |- channels.html            
    |- static
    |- scripts.py

```


---

## View Static

Assembly uses Flask-Assets to help manage static assets, ie: images, js, css in your application

