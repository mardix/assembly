# Assembly

### A Pythonic Object-Oriented Web Framework built on Flask

--- 

**Assembly** is a pythonic object-oriented, mid stack, batteries included framework built on Flask, that adds structure 
to your Flask application, and group your routes and endpoints by class.

**Assembly** allows developers to build web applications in much the same way they would build any other object-oriented Python program. 

Technically **Assembly** is an attempt of making a simple framework based on Flask Great Again!

---

[Documentation](https://mardix.github.io/assembly)

---

## First Assembly! 

```
# views.py

from assembly import Assembly, response, request, HTTPError

# Extends to Assembly makes it a route automatically
# By default, Index will be the root url
class Index(Assembly):

    # index is the entry route
    # -> /
    index(self):
        return "welcome to my site"

    # method name becomes the route
    # -> /hello/
    hello(self):
        return "I am a string"

    # undescore method name will be dasherize
    # -> /about-us/
    about_us(self):
        return "I am a string"


# The class name is part of the url prefix
# This will become -> /blog
class Blog(Assembly):
    
    # index will be the root 
    # -> /blog/
    index(self):
        return [
            {
                "title": "title 1",
                "content": "content"
            },
            ...
        ]

    # with params. The order will be respected
    # -> /comments/1234/
    # 1234 will be passed to the id
    comments(self, id):
        return [
            {
                comments...
            }
        ]


# It's also Restful
class Api(Assembly):

    # method named get, automatically accepts get method
    # -> GET /api/
    get(self):
        return {
            "message": "This will show on get call"
        }

    # method named post, automatically accepts post method
    # -> POST /api/
    post(self):
        return {
            "message": "This will show on POST call"
        }

    # Can change the response to json
    # -> /api/about/
    @response.json
    about(self): 
        return {
            "name": "Assembly",
            "version": "1.0.1"
        }

    # endpoint with different method 
    # -> POST /api/submit/
    @request.post
    submit(self):
        return {
            "message": "This will show on POST call only"
        }

    # This will throw an Unauthorize error
    error(self):
        raise HTTPError.Unauthorized()

```


---

## Decisions made for you + Features

- Smart routing: automatically generates routes based on the classes and methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at '/user-account'

- Class methods (action) could be accessed: hello_world(self) becomes 'hello-world'

- Smart Rendering without adding any blocks in your templates

- Auto rendering by returning a dict of None


- Templates are mapped as the model in the class the $module/$class/$method.html

- Markdown ready: Along with  HTML, it can also properly parse Markdown

- Auto route can be edited with @route()

- Restful: GET, POST, PUT, DELETE

- REST API Ready

- bcrypt is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- ORM: [Active-Alchemy](https://github.com/mardix/active-alchemy) (SQLALchemy wrapper)

- Uses Arrow for dates 

- Active-Alchemy saves the datetime as arrow object, utc_now

- CSRF on all POST

- CloudStorage: Local, S3, Google Storage [Flask-Cloudy](https://github.com/mardix/flask-cloudy)

- Mailer (SES or SMTP)

- Caching



## Quickstart

#### Install Assembly

To install Assembly, it is highly recommended to use a virtualenv, in this case I 
use virtualenvwrapper 

    mkvirtualenv my-assembly-site

Install Assembly

    pip install assembly
    
#### Initialize your application

Now Assembly has been installed, let's create our first application

```
    cd your-dir
    
    asm-admin init
```


`asm-admin init` setup the structure along with the necessary files to get started

### Hello World

```

from assembly import (Assembly, response)

class Index(Assembly):
    
    index(self):
        return "Hello World"

    @response.json
    api(self):
        return {
            "name": "Assembly",
            "version": "x-to-infinity"
        }


```

 You will see a structure similar to this
 
    /your-dir
        |
        |__ .gitignore
        |
        |__ app.json
        |
        |__ requirements.txt
        |
        |__ assembly.py
        |
        |__ application/
            |
            |__ __init__.py
            |
            |__ config.py
            |
            |__ /models/
                |
                |__ __init__.py
                |
                |__ models.py
            |
            |__ /views/
                |
                |__ __init__.py
                |
                |__ main.py
            |
            |__ /templates/
                | 
                |__ /layouts/
                    | 
                    |__ base.jade
                |
                |__ /main/
                    |
                    |__ /Index/
                        |
                        |__ index.jade
            |
            |__ /static/
                |
                |__ assets.yml
                |
                |__ package.json
            |
            |__ /data/
                |
                |__ babel.cfg
                |
                |__ /uploads/
                |
                |__ /babel/
                |
                |__ /mail-templates/
            |
            |__ /lib/


 
#### Serve your first application

If everything is all set, all you need to do now is run your site:

    asm-admin server
    
It will start serving your application by default at `127.0.0.1:5000`

Go to http://127.0.0.1:5000/ 

---

I hope this wasn't too hard. Now Read The Docs at [http://mardix.github.io/assembly/](http://mardix.github.io/assembly/)
for more 

Thanks, 

Mardix :) 

--- 

## Read The Docs

To dive into the documentation, Read the docs @ [http://mardix.github.io/assembly/](http://mardix.github.io/assembly/)

---

License MIT

Copyright: 2019 - Forever Mardix

