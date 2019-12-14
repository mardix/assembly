
## Deploy Options

To get a comprehensive deploy options with Assembly, please follow <a href="https://flask.palletsprojects.com/en/1.1.x/deploying/" target="_blank">**Deploying Options**</a> with Flask. Assembly is actually Flask, so everything on the link is valid for Assembly.

Below are some of the options you would be interested in.

---

### Environment Variable

**Note**: When deploying, make sure you set the right environment 

```sh
export ASSEMBLY_APP=default
export ASSEMBLY_ENV=Development
```

---


### Gunicorn

Gunicorn ‘Green Unicorn’ is a WSGI HTTP Server for UNIX. It’s a pre-fork worker model ported from Ruby’s Unicorn project. It supports both eventlet and greenlet.

```sh
export ASSEMBLY_APP=default
export ASSEMBLY_ENV=Production
gunicorn -w 4 wsgi:app
```


---

### uWSGI

uWSGI is a fast application server written in C. It is very configurable which makes it more complicated to setup than gunicorn.

```
export ASSEMBLY_APP=default
export ASSEMBLY_ENV=Production
uwsgi --http 127.0.0.1:5000 --module wsgi:app
```

---

### Heroku

Set the environment variables for Heroku

```
heroku config:set ASSEMBLY_ENV=Production
heroku config:set ASSEMBLY_APP=default
```

 **Edit *PROCFILE***

```
web: gunicorn wsgi:app
release: asm gen:sync-models; asm setup 
```

---

### Boxie

Unlike Gunicorn and uWSGI, Boxie gives you something more like a PaaS (Platform as a Service) option. If you manage your own server, we recommend Boxie and you will love it :).

**Boxie** is a utility to install on a host machine, that allows you to deploy multiple sites or apps, run scripts and background workers on a single VPS, Digital Ocean or Linode instance.

**Boxie** follows a process similar to Heroku or Dokku where you push code to the host via Git, and **Boxie** will:
- create an instance on the host machine
- deploy the new code
- create virtual environments for your application
- get a free SSL from LetsEncrypt and assign it to your domain
- execute scripts to be executed
- put your application online
- monitor the application
- restart the application if it crashes

Learn more about <a href="https://github.com/mardix/boxie" target="_blank">**Boxie**</a>

Boxie configuration is already shipped with Assembly, with `boxie.yml`. 

`boxie.yml` is a manifest format for describing apps. It declares environment variables, scripts, and other information required to run an app on your server.


```yml
---
name: My Assembly App
description: my awesome app in Assembly
version: 1.0.0
apps:
  - name: yourdomain.com
    server_name: yourdomain.com
    runtime: python
    auto_restart: true
    env:
      ASSEMBLY_ENV: Production
      ASSEMBLY_APP: default
    scripts:
      release:
        - asm gen:sync-models
        - asm setup
    process:
      web: wsgi:app
```

