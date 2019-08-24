

# Mocha

---

 <div style="text-align:center">
 <h2>A batteries included, front-end loaded, web and Restful framework built on Flask.</h2>
 </div>


![Mocha](/img/cup3.jpg)

Mocha helps you build and structure your application, where your endpoints are natively created from your view names.

If you already know Flask, you pretty much know 95% of Mocha.

---

## <div style="text-align:center">Quick Start</div>

#### Install

    pip install mocha

#### Setup


    mocha :init


#### Serve

    mocha :serve

---

## <div style="text-align:center">Features</div>

### **Class based views**

Mocha groups your views together by class. The class name becomes the base route of all the methods.
Mocha expects the methods to return dict.

    from mocha import Mocha

    class Index(Mocha):
        def index(self):
            return {
                "name": "Mocha",
                "version": "1.0"
            }

        def hello_world(self):
            return {
                "hello": "world"
            }

    class Document(Mocha):
        def index(self):
            return

        def about(self):
            return


---

### **Smart Routing**

Smart routing is created by using the class name and the method name. Class or method named `Index` or `index` respectively,
will become the root; otherwise the class name will be the base root name, and all of its methods will be prefixed with it.

    from mocha import Mocha

    class Index(Mocha):

        def index(self):
            # -> http://127.0.0.1/

            return {
                "name": "Mocha",
                "version": "1.0"
            }

        def hello_world(self):
            # -> http://127.0.0.1/hello-world

            return {
                "hello": "world"
            }

    class Account(Mocha):

        def index(self):
            # -> http://127.0.0.1/account

            return {
                "name": "Mocha",
                "version": "1.0"
            }

        def info(self):
            # -> http://127.0.0.1/account/info

            return {
                "name": "Mardix"
            }

    class Document(Mocha):

        def index(self):
            # -> http://127.0.0.1/document/

            return {
                "docs": [

                ]
            }

        def get(self, id):
            # -> http://127.0.0.1/document/1234
            return {
                "title": "Doc title"
            }

---

### **Custom Route**

Just like Flask, you can use the `mocha.route` decorator for custom routes. If the the class is decorated, all the
the methods will inherit the parent route.


    from mocha import Mocha, decorators as deco

    @deco.route("/the-great-catalog")
    class Catalog(Mocha):

        @deco.route("/list/")
        def index(self):
            # -> http://127.0.0.1/the-great-catalog/lists

            return {
                "my_collections": [
                    {
                        "id": 123,
                        ...
                    },
                    ...
                ]
            }

---

### **RESTful**

Mocha has some reserved methods name: `get`, `post`, `put`, `delete`, `update`. They required the `request.method`  to be
the same as the name. By default all other methods are `GET`

    from mocha import Mocha

    class Index(Mocha):

        def index(self):
            # -> http://127.0.0.1/

            return {
                "name": "Mocha",
                "version": "1.0"
            }

        def get(self, id):
            # Accepts only GET method
            # GET http://127.0.0.1/894

            return {
            }

        def post(self, id):
            # Accept only POST method
            # POST http://127.0.0.1/894
            # do something in post

        def delete(self, id):
            # Accept only DELETE method
            # DELETE http://127.0.0.1/894
            # do something in delete

        def put(self, id):
            # Accept only PUT
---


### **Multiple renders: JSON, XML**

You can quickly render your views to json or xml. By default it's HTML


    from mocha import Mocha, decorators as deco

    @deco.render_json
    class Index(Mocha):

        def index(self):
            return {
                "name": "Mocha",
                "version": "1.0"
            }

        def hello_world(self):
            return {
                "hello": "world"
            }

    class Catalog(Mocha):

        def index(self):
            return {
                "my_collections": [
                    {
                        "id": 123,
                        ...
                    },
                    ...
                ]
            }

---

### **Built-in Nav Title**


As you are creating your views, you can also build the navigation menu, by using `@decorators.nav_title`


    from mocha import Mocha, decorators as deco

    @deco.nav_title("The Great Catalog")
    class Catalog(Mocha):

        @deco.nav_title("All")
        def index(self):
            return {
                "my_collections": [
                    {
                        "id": 123,
                        ...
                    },
                    ...
                ]
            }


---

### **Admin**

Mocha allows you to quickly turn your views into restricted admin area.

Accessing `http://127.0.0.1/admin/catalog` will require you to login

    from mocha import Mocha, decorators as deco
    import mocha.contrib

    @deco.nav_title("Catalog")
    @deco.route("/admin/catalog")
    @mocha.contrib.admin
    class CatalogAdmin(Mocha):

        @deco.nav_title("All")
        def index(self):
            return {
                "my_collections": [
                    {
                        "id": 123,
                        ...
                    },
                    ...
                ]
            }

---

### **Interceptors**

Sometimes you may want to do something before or after request, Mocha helps you with that.

    from mocha import Mocha

    class Index(Mocha):

        def before_request(self, name, *args, **kwargs):
            pass

        def after_request(self, name, response):

            return response

---

### **Jade markup**

For aesthetic reason, Mocha uses by default Jade (now Pug) template. This can switched if you want to use HTML file only

    .row
        .col-md-12
            h1.text-center
                | Hello Mocha


Becomes

    <div class="row">
        <div class="col-md-12">
            <h1 class="text-center">
                Hello Mocha
            </h1>
        </div>
    </div>


---

### **Markdown friendly**




---

### **Built-in contrib**

- User Auth : It allows to authenticate users into the application. Contains the following pages:
    - login
    - signup
    - lost-password
    - account-settings
    - admin interface

- Contact Us

- Error: Error pages

- Admin Interface: Create authenticated admin area

- Maintenance page: To turn the site on and off

---


## Features List

- Smart routing: automatically generates routes based on the classes and methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at '/user-account'

- Class methods (action) could be accessed: hello_world(self) becomes 'hello-world'

- Easy rending and render decorator

- Auto route can be edited with @route()

- Restful: GET, POST, PUT, DELETE

- REST API Ready

- Jade as default template language

- Markdown friendly. Inclusion of a markdown file will turn into HTML

- `bcrypt` is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- Database/ORM: [Active-Alchemy](https://github.com/mardix/active-alchemy) (SQLALchemy wrapper)

- ReCaptcha: [Flask-Recaptcha](https://github.com/mardix/flask-recaptcha)

- CSRF on all POST

- Storage: Local, S3, Google Storage [Flask-Cloudy](https://github.com/mardix/flask-cloudy)

- Mailer (SES or SMTP)

- Arrow for date and time

- Caching



- JWT

- Pagination

- Signals

- Fontawesome

- Bootstrap 3

- Bootswatch

- Markdown



- Propel for deployment



- Smart routing: automatically generates routes based on the classes and methods in your views

- Class name as the base url, ie: class UserAccount will be accessed at '/user-account'

- Class methods (action) could be accessed: hello_world(self) becomes 'hello-world'

- Smart Rendering without adding any blocks in your templates

- Auto rendering by returning a dict or None

- Use Jade (Pug) template by default, but you can also use HTML.

- Templates are mapped as the model in the class the $module/$class/$method.jade

- Markdown ready: Along with Jade and HTML, it can also properly parse Markdown

- Auto route can be edited with @route()

- Restful: GET, POST, PUT, DELETE

- REST API Ready

- `bcrypt` is chosen as the password hasher

- Session: Redis, AWS S3, Google Storage, SQLite, MySQL, PostgreSQL

- ORM: [Active-Alchemy](https://github.com/mardix/active-alchemy) (SQLALchemy wrapper)

- ReCaptcha: [Flask-Recaptcha](https://github.com/mardix/flask-recaptcha)

- Arrow for dates

- Active-Alchemy for database and dates are saved as Arrow object

- All dates are by default UTC

- Date can be presented in specific timezone

- CSRF on all POST

- Storage: Local, S3, Google Storage [Flask-Cloudy](https://github.com/mardix/flask-cloudy)

- Mailer (SES or SMTP)

- Caching

- Signals to dispatch messages and data to other part of the application

- JWT

- Default Layout

- Admin interface

- Multi application

- Web Assets

- Propel for deployment

- Decorators, lots of decorators

---

## Packages and utilities depencies:

- Flask
- Flask-Assets
- cssmin
- jsmin
- flask-recaptcha
- flask-login
- flask-kvsession
- flask-s3
- flask-mail
- flask-caching
- flask-cloudy
- flask-seasurf
- flask-babel
- flask-cors
- Flask-OAuthlib
- Active-Alchemy
- Paginator
- six
- passlib
- bcrypt
- python-slugify
- humanize
- redis
- ses-mailer
- markdown
- inflection
- pyyaml
- click
- sh
- dicttoxml
- arrow
- blinker
- itsdangerous
- pyjade
- requests


---

Credits: Flask, Flask-Classy