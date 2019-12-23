
## Setup Assembly

**Install**

`pip install assembly`

**Initialize**

`asm gen:init`

**Run Development Server**

`asm gen:serve`

---

## REST API

**Generate the view using `asm` generator**

`asm gen:views my-api --restful`

This will generate a module at `/views/api.py`

**Import in wsgi.py**

```
# wsgi.py

APPS = {
  "default": [
    "views.main",
    "views.api"
  ]
}
```

**Edit View**

```python

# views/api.py

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

**Generate the view using `asm` generator**

`asm gen:view admin`

This will generate a module at `/views/admin.py`. And its associated templates at `/templates/admin/Index/index.html`

**Import in wsgi.py**

```sh

# wsgi.py

APPS = {
  "default": [
    "views.main",
    "views.admin"
  ]
}
```

**Edit your first view**

```python

# views/admin.py

from assembly import (Assembly, response)

@response.route("/admin/")
class Index(Assembly):
    
    def index(self):
        return {
            "title": "Assembly is awesome",
            "content": "That is a true fact"
        }


```


**Edit Index/index.html**

```html

<!-- templates/main/Index/index.html -->

{% extends 'layouts/base.html' %}

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

---

## Login Manager

---

## Forms

---