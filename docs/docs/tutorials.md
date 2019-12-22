
## Setup Assembly

**Install**

`pip install assembly`

**Initialize**

`asm gen:init`

**Run Development Server**

`asm gen:serve`

---

## REST API

**Generate the view using asm **

`asm gen:resful-module my-api`

This will generate a Module package with `views.py`, `models.py`, `scripts.py`.

**Import in wsgi.py**

```
# wsgi.py

APPS = {
  "default": [
    "modules.main",
    "modules.api"
  ]
}
```

**Edit View**

```python

# modules/api/__views__.py

from assembly import (Assembly, request, response, date)

@response.route("/api/")
class Index(Assembly):

  @response.json
  def index(self):
    return {
      "date": date.utcnow()
    }

  @request.post
  def submit_info(self):
    return {
      "message": "Thank you"
    }

```

---

## HTML Site

**Generate the view using asm-admin**

`asm gen:template-module admin`

This will generate a View package with `views.py`, `models.py`, `templates/`, `static/`, `scripts.py`.

**Import in wsgi.py**

```sh

# wsgi.py

APPS = {
  "default": [
    "modules.main",
    "modules.admin"
  ]
}
```

**Edit your first view**

```python

# modules/admin/views.py

from assembly import (Assembly, response)

@response.route("/admin/")
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


**Edit Index/index.html**

```html

<!-- modules/admin/templates/Index/index.html -->

{% extends 'modules/main/layouts/base.html' %}

{% block title %}Welcome to Admin {% endblock %}

{% block body %}
    <div>
        <h1>{{ title }}</h1>
    </div>
    <div>
        {{ content }}
    </div>
{% endblock %}
```


**Serve your first application**

If everything is all set, all you need to do now is run your site:

```
asm gen:serve
```

It will start serving your application by default at `127.0.0.1:5000`

Two endpoints will be available:

- `http://127.0.0.1:5000/admin` which will show an HTML
- `http://127.0.0.1:5000/admin/api/` which will a json response



---

## Error Handler



---

## Work with CORS API


---

## Create Custom CLI

---

## Work with CSRF

---

## Upload Application

