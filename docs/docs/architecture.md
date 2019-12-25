
## Overview

Assembly tries to keep it simple by providing a flat structure for your application and gives you the freedom to do whatever else. 

It lays out a basic layout, so the application can be consistent. 

---

## Structure

A basic application structure looks like this

```sh
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
      |- js
      |- css
      |- imgs
    |- data/

```


### Structure Description

- `wsgi.py` is the application object. (required)

- `requirements.txt`: contains application dependencies including `assembly` (required)

- `lib` contains config and models, including shared modules (directory required)

- `run` contains scripts and executable files to run

- `views`: a directory containing the view modules. It must contain  `__init__.py`

- `templates`: contains the HTML templates associated to the views from `/views`. 

- `static`: contains the images, js, css or any non user-generated files. 

- `data`: a directory containing various data, uploads, etc, including user-generated files.


---

### Default View Structure

By default Assembly will be initialized with `/views`, which contains the modules having classes extending `Assembly`.

The view package is simply a package/directory that contains a `__init__.py` and can be imported into the `APPS` list in the `wsgi.py` file. 

*You can also create View Component to have distributable or shared package to import, learn more about it below.* 

The view name is the folder. The example below show the `main` view.

```sh
|- views/
  |- __init__.py
  |- main.py
|- templates
    |- main/
      |- Index
          |- index.html
    |- layouts
        |- base.html

```
---

## View Class structure

To create a View class, all you need is to create classes that extends `Assembly`, and Assembly will make it routable and behave the right way.

You will need to import the modules either by importing them in the `__init__.py` or APPS list in the `wsgi.py`

```python
# views/main.py

from assembly import Assembly

class Index(Assembly):
  def index(self):
    return

```

---

### Multiple Classes

You can have multiple classes in a single view file, ie: `main.py`. They will be treated properly with the proper endpoint.

```python

# views/main.py

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

### Routes and Entry Points

There are some rules  around the routes and endpoints.

Assembly will automatically use the class name as the ROUTE, and the method names as SUB ROUTE.

- Classes named **Index** will be used as the ENTRY POINT. Method with the name **index** will be used the 

- Classes name in  UpperCamelCase, will be routed to the dasherize name of the class. 

- Method with under_score will be routed to the dasherized of the method.

```python

# responds to /
class Index(Assembly):
  def index(self):
    return

  # /about
  def about(self):
    return 

# responds to /api/
class Api(Assembly):
  def index(self):
    return


# responds to /admin/
class Admin(Assembly):
  def index(self):
    return

  def settings(self):
    return 

class SuperHero(Assembly):
  def index(self):
    return 

  def contact_us(self):
    return

```

- `Index.index` will respond to `/`

- `Index.about` will respond to `/about`

- `Api.index` will respond to `/api` 

- `Admin.index` will respond to `/admin` 

- `Admin.settings` will respond to `/admin/settings` 

- `SuperHero.index` will respond to `/super-hero`

- `SuperHero.contact_us` will respond to `/super-hero/contact-us`


---

### Namespace

Everything is properly namespaced, however the only time you may see some clashes is when more than one class has the same class name. To fix that, just use a different **route endpoint** for the class.

```python
# views/main.py

from assembly import Assembly

# responds to /
class Index(Assembly):
  def index(self):
    return 

---

# views/admin.py

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
# views/main.py

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
|- templates
  |- main/
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
```


---

## View Static

Assembly uses Flask-Assets to help manage static assets, ie: images, js, css in your application


---

## View Component

Similar to the default `/views` package that gets generated by Assembly, you can create a distributable or reusable package name **View Component**. 

```

|-/my_view_component
  |- __init__.py
  |- main.py
  |- models.py
  |- templates/
    |- Index
      |- index.html
  |- static/
    |- js
    |- css

```


