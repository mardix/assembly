
## Overview 

**wsgi.py** is the application's entry point which contains the application object called `app`

`wsgi.py` and `app` are both required. 

---

## wsgi.py

```python
# wsgi.py

from assembly import Assembly

APPS = {
  "default": [
    "views.main"
  ]
}

app = Assembly.initialize(__name__, APPS)
```

---

### app

`app` is the application object. It's a Flask object actually.

---

### \_\_name__

`__name__` is a special variable that gets as value the string "__main__" when the file gets executed.

---

### APPS

Assembly is a multi-application framework, where you can launch different application with the same code base.

To achieve this, Assembly requires a list off all the views to be used per app.

Upon deploying an app, you can select on by providing the name of it using the environment variable `ASSEMBLY_APP`.

---


## Environment Variables

Having set `wsgi.py` properly you will be able to load different apps using the environment variables.

### ASSEMBLY_APP

`export ASSEMBLY_APP=$appname`, where $appname is name from the `APPS` list. 
 
### ASSEMBLY_ENV

`export ASSEMBLY_ENV=$configClassName`, where $configClassName is a class name from `config.py`.

---

## Deployment


To deploy your application, learn more about **[Deploy Options](deploy.md) **


