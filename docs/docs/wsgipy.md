
**wsgi.py** is the application's entry point 



## Initialize

```
# wsgi.py

from assembly import Assembly

APPS = {
  "default": [
    "main"
  ]
}

app = Assembly.initialize(__name__, APPS)
```

### app

### \_\_name__

### APPS

Assembly is a multi-application framework, where you can launch different application in the same code base.

To achieve this, Assembly requires a list off all the views to be used per app.

Upon deploying an app, you can select on by providing the name of it using the environment variable `ASSEMBLY_APP`.

```


```


## Environment Variables

### ASSEMBLY_APP

### ASSEMBLY_ENV

