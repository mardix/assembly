# Assembly


### 1. Set environment variables

```
export ASSEMBLY_ENV=Development # for development
export ASSEMBLY_PROJECT=default  # for prod
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
        |-- __views__.py
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

```

## Serve your app

```
asm-admin server
```

**wsgi.py**

**config.py**

**${application}**

**${application}/__views__.py**

**${application}/__models__.py**

**${application}/templates**

**${application}/static**



## app.json


