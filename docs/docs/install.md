

Assembly is a Pythonic Object-Oriented Web Framework built on Flask

---

### Requirements

- Python 3.6+
- Virtualenv

---

### Install

Install Assembly with `pip install assembly`

It is highly recommended to use a virtualenv, in this case let's
use VirtualenvWrapper (you can use any that is convenient for you)

```
mkvirtualenv my-first-app

workon my-first-app

pip install assembly

```

---

### Initialize

Initialize Assembly with `asm-admin init`

CD into the folder you intend to create the application, then run `asm-admin init`. 
This will setup the structure along with the necessary files to get started



```
cd app-dir

asm-admin init

```
---

### Structure

Upon initialization you should have a structure similar to this:

```
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- app.json
    |- __data__  
    |- main
        |- __init__.py
        |- __models__.py
        |- templates
            |- Index
                |- index.html
            |- layouts
                |- base.html
        |- static
        |- cli.py

```

#### Base files and folders

```
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
    |- app.json
    |- __data__  
```

- `wsgi.py` is the application object. (name required)

- `config.py`: contains class based configurations (name required)

- `requirements.txt`: contains application dependencies including `assembly`

- `app.json`: Application manifest to deploy using Gokku

- `__data__`: A variable directory, to put misc files, uploads, etc.


#### Application's View Structure

Views are simply a directory that contains at least `__init__.py` and can be imported into the `APPS` list in the `wsgi.py` file. 

Additionally, you can find `__models__.py`, `templates/`, `static/`

The view name is the folder. The example below show the `main` view.


```
|- main
    |- __init__.py
    |- __models__.py
    |- templates
        |- Index
            |- index.html
        |- layouts
            |- base.html
    |- static
    |- cli.py

```

- `main` view directory

- `__init__.py` Loaded implicitely, contains all the view classes
- `__models__.py` loaded implicitely, contains all the Models for that View
- `templates` contains templates for the each endpoint in the `__init__.py` view.
- `static` contain the static files, images, css, js, etc.
- `cli.py` Custom CLI for that view.

