# Assembly


### 1. Set environment variables

```
export ASSEMBLY_ENV=Development # for development
export ASSEMBLY_APP=default  # for prod
```

### 2. Run the wsgi
```
wsgi:app
```

---

## Directory Structure

```

    #ROOT
    |
    |-- wsgi.py
    |
    |-- config.py
    |
    |-- app.json
    |
    |-- requirements.txt
    |
    |-- /${application}
        |
        |-- __init__.py
        |
        |-- __models__.py
        |
        |-- cli.py
        |
        |-- templates
            |-- Index/
                |-- index.html
        |
        |-- static
            |-- images
            |-- css
            |-- js
            |-- assets.yml
    |- __dir__

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


