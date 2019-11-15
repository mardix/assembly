# Assembly


### 1. Set environment variables

```
export ASSEMBLY_ENV=Development # for development
export ASSEMBLY_APP=default  
```

### 2. Run the wsgi
```
wsgi:app
```

---

## Directory Structure


```
-- /
    |- wsgi.py
    |- config.py
    |- requirements.txt
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

    |- __data__
```


## Serve your app

```
asm-admin serve
```

**wsgi.py**

**config.py**

**${application}**

**${application}/__init__.py**

**${application}/__models__.py**

**${application}/templates**

**${application}/static**



## app.json


