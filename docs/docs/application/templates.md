
## Overview

Assembly uses Jinja as template language, files are organized per Class and Methods name.


## Structure

Files are organized per Class and Methods name.  Each class name have corresponding **folder** with the same name, and every method have a corresponding **.html** with the same name inside of the folder.


Having a View like this...

```python
# views/admin.py

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
|- views/
    |- __init__.py
    |- admin.py
|- templates/
    |- admin/
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

-- IN CONSTRUCTION --