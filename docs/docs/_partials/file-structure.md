    /____
        |
        |- brew.py
        |
        |- propel.yml
        |
        |-- requirements.txt
        |
        |-- /application
            |
            |-- config.py
            |
            |-- models.py
            |
            |-- helpers.py
            |
            |-- manage.py
            |
            |-- views/
                |
                |-- main.py
            |
            |-- templates/
                |
                |-- layouts/
                    |
                    |-- base.jade
                    |
                |-- main/
                    |
                    |-- Index/
                        |
                        |-- index.jade
            |
            |-- /static/
                |
                |-- assets.yml
                |
                |-- package.json
                |
                |-- css/
                |
                |-- js/
                |
                |-- imgs/
            |
            |-- /var/

Description:

- `brew.py` is the application entry point
- `propel.yml` (optional) A deploy based config file
- `requirements.txt` contains your requirements + mocha
- `application/` contains the application's  models, config, helpers and manage
- `application/views/`: contains your views modules
- `application/templates/`: contains all templates relative to the views name
- `application/static/`: contains all the app's assets: js, css, imgs, etc...
- `application/var/`: contains var files: database, mail-template, uploads, etc...



