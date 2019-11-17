
## Setup Assembly

**Install**

`pip install assembly`

**Initialiaze**

`asm-admin init`

**Run Development Server**

`asm-admin serve`

---

## REST API

**Generate the view using asm-admin**

`asm-admin gen-api-view my-api`

This will generate a View package with `__init__.py`, `__models__.py`, `cli.py`.

**Import in wsgi.py**

```
# wsgi.py

APPS = {
  "default": [
    "main",
    "api"
  ]
}
```

**Edit View**

```
# /api/__init__.py

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

`asm-admin gen-template-view admin`

This will generate a View package with `__init__.py`, `__models__.py`, `templates/`, `static/`, `cli.py`.

**Import in wsgi.py**

```
# wsgi.py

APPS = {
  "default": [
    "main",
    "admin"
  ]
}
```

**Edit your first view**

```

# admin/__init__.py

from assembly import (Assembly, response)

@response.route("/admin/")
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


**Edit Index/index.html**

```
<!-- admin/templates/Index/index.html -->

{% extends 'main/layouts/base.html' %}

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
asm-admin serve
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

