## Overview

Core methods and functions


## Functions


### Assembly

```python
from assembly import Assembly
```


### config

```python
from assembly import config
```

### env

```python
from assembly import env
```

### ext 

```python
from assembly import ext
```

### db


```python
from assembly import db
```

### models

```python
from assembly import models
```

Holds all class models that have been extended by `db.Model`. 

To use, access them via `models.{ModelName}`

```python
from assembly import models

class Index(Assembly):

  def index(self):
    user = models.User.query()

```

### views

```python
from assembly import views
```

### date

```python
from assembly import date
```

### set_cookie

```python
from assembly import set_cookie
```

### get_cookie

```python
from assembly import get_cookie
```

### delete_cookie

```python
from assembly import delete_cookie
```

### url_for

```python
from assembly import url_for
```

### redirect

```python
from assembly import redirect
```

---

## Decorators

### decorate

Applies a decorator, usually a 3rd party decoartor to all method in the class

```python
from assembly import decorate
from flask_login import login_required

@decorate(login_required)
class Login(Assembly):
  def index(self):
    return 

```

### app_context

```python
from assembly import app_context
```








