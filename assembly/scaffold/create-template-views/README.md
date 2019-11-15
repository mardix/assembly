
# Assembly Template View

Assembly is composed of 
- `__init__` contains the views
- `__models__` contains the models
- `templates` contains the HTML template
- `static` contains the static assets: css, js, images, etc.

---

## Views

`__init__` contains class based views extended by `Assembly`. Views are loaded implicitely. 

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

`__models__` contains your models. Models are loaded implicitely.

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

For convenience, you can use the main base layout from `main/layouts/base.html` for the layout of the page

### Extends base layout

Extends the base layout in the pages

```
{% extends 'main/layouts/base.html' %}
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

