
# Assembly API View

Assembly is composed of 
- `__views__` contains the views
- `__models__` contains the models

---

## Views

`__views__` contains class based views extended by `Assembly`. Views are loaded implicitely. 

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



