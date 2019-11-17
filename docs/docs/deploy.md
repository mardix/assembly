
## Deploy Options

To get a comprehensive deploy options with Assembly, please follow <a href="https://flask.palletsprojects.com/en/1.1.x/deploying/" target="_blank">**Deploying Options**</a> with Flask. Assembly is actually Flask, so everything on the link is valid for Assembly.

Below are some of the options, you would be interested in

---



### Gunicorn

Gunicorn ‘Green Unicorn’ is a WSGI HTTP Server for UNIX. It’s a pre-fork worker model ported from Ruby’s Unicorn project. It supports both eventlet and greenlet.

```text
gunicorn -w 4 wsgi:app
```


---

### uWSGI

uWSGI is a fast application server written in C. It is very configurable which makes it more complicated to setup than gunicorn.

```text
uwsgi --http 127.0.0.1:5000 --module wsgi:app
```

---

### Gokku

**Gokku** is a very small PaaS to do git push deployments to your own servers (Digital Ocean, Linode) similar to Heroku.

Learn more about <a href="https://github.com/mardix/gokku" target="_blank">**Gokku**</a>

Gokku configuration is already shipped with Assembly, with `app.json`. The `app.json` will launch your website from 0 to 100 just like it would on Heroku. 

At the root  of the application, **app.json** is a manifest format for describing web apps. It declares environment variables, scripts, and other information required to run an app on your server.

```
{
  "name": "domain.com",
  "version": "0.0.1",
  "description": "my application domain.com",
  "gokku": {
    "domain_name": "domain.com",
    "runtime": "python",
    "auto_restart": true,
    "env": {
      "ASSEMBLY_ENV": "Production",
      "ASSEMBLY_APP": "default"
    },
    "scripts": {
      "release": [
        "asm-admin sync-models",
        "asm setup"
      ]
    },    
    "run": {
      "web": "wsgi:app"
    }
  }
}
```

