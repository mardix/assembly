# Assembly


### 1. Set environment variables

```
export ASSEMBLY_ENV=Development # for development
export ASSEMBLY_APP=default  
```

### 2. Run the wsgi
```
wsgi:app
```

---

## Directory Structure


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
        |- error.py
    |- templates/
        |- main/
            |- Index/
                |- index.html
        |- error/
            |- Error
                |- error_404.html
                |- error_handler.html
    |- static/
    |- data/

```


## Serve your app

```
asm-admin serve
```

**wsgi.py**

**config.py**

**${application}**

**${application}/__init__.py**

**${application}/__models__.py**

**${application}/templates**

**${application}/static**



## app.json

---

## Application

# Assembly Template View

Assembly is composed of 
- `lib` contains shared libraries, config and models
- `run` contains scripts to execute
- `views` contains the views
- `models` contains the models
- `templates` contains the HTML template
- `static` contains the static assets: css, js, images, etc.

---

## Views

`views` contains class based views extended by `Assembly`. Views are loaded implicitely. 

```

from assembly import Assembly

class Index(Assembly):
  def index(self):
    return {
      "title": "Hello World"
    }

```

---

## Models

`models` contains your models. Models are loaded implicitely.

```
from assembly import db

class Test(db.Model):
    name = db.Column(db.String(255), index=True)

```


---

## Template

Assembly uses Jinja2 as templating language. 

`/templates` contains the views templates where class name and the method, match the folder and the file respectively. Example:

```
  class Index(Assembly):
    def about_us(self):
      return
```

will match the template `Index/about_us.html`

---

## Using Base Layout

For convenience, you can use the main base layout from `layouts/base.html` for the layout of the page

### Extends base layout

Extends the base layout in the pages

```
{% extends 'layouts/base.html' %}
```

### Block title

`{% block title %}...{% endblock %}` to set page title

```
{% block title %}Page Title{% endblock %}
```

### Block body

`{% block body %}...{% endblock %}` the main body of the page

```
{% block body %}
    <div>
      something...
    </div>
{% endblock %}
```

### Block header

`{% block header %}...{% endblock %}` for header content

### Block footer

`{% block footer %}...{% endblock %}` for footer content

### Block sidebar

`{% block sidebar %}...{% endblock %}` for sidebar content

---

## Static

`static/` contains the static files to be used.


---



