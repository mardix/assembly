
If you haven't done so yet, you need to `mocha :init` in the directory that you want to install

    mocha :init

Once created, you should see a file structure similar to this


{!_partials/file-structure.md!}

---

## Your first app

Here's what Mocha will do, and expecting:

- that your views are structured in class
- the class inherits `mocha.Mocha`
- if the class name is `Index(Mocha)`, it will be the base route as `/`
- the methods are the views actions
- the methods name will become the endpoint url
- if the method name is `index(self)`, it will be the entry point of that view
- methods name with underscore will be dasherized, `about_us(self)` -> `/about-us/`
- the methods return data as dict type
- the data returned is passed to your template
- the template is named after the method name
- the template is magically included in your layout
- Mocha brews everything together, and renders the page


---

## Views


All your view module should be placed in `application/views`. By default , `main.py` view is created

`main.py` must contain at a least one class that inherits `Mocha`. A view module may have multiple classes


`application/views/main.py`

    from mocha import Mocha, page_attr

    class Index(Mocha):

        def index(self):
            page_attr("Hello World")
            return  {
                "name": "Mocha",
                "version": "1.0"
            }

        def about_us(self):
            page_attr("About Us")
            return


    class Document(Mocha):

        def index(self):
            page_attr('All documents')
            return {
                "docs": [
                    {
                        "id": 1,
                        "title": "This is a doc title"
                    },
                    ...
                ]
            }

        def get(self, id):
            page_attr("This is a doc title")
            return {
                "id": id,
                "title": "This is a doc title",
                "content": "My content"
            }


The `main.py` module contains two view classes: Index and Document that inherit `Mocha`.
Also imported `page_attr`, a utility function to set the page title and other page attributes

The methods return `dict` or `None`

The route will be created from the class and method name.

If the class name is `Index`, it will be the root of the domain, in this example `/`, and other will stay as is,
in this instance the `Document` will have as route `/document/`.

The following url will be created:

- `Index:index()` -> `http://localhost:5000/`
- `Index:about_us()` -> `http://localhost:5000/about-us`
- `Document:index()` -> `http://localhost:5000/document`
- `Document:get(id)` -> `http://localhost:5000/document/1234`

---

## Template

All your templates should be placed in `application/templates`. And must follow the same directory
structure relative to the view modules. The returned data from the view will be passed to the template.

So for `application/views/main.py`, it is expecting the following template structure

    /application
        |
        |-- templates
            |
            |
            |-- main/
                |
                |-- Index/
                    |
                    |-- index.jade
                    |
                    |-- about_us.jade
                |
                |__ Document/
                    |
                    |-- index.jade
                    |
                    |-- get.jade


As you can see, the template structure follows the view structure, where in the view:

- `main.py` -> /templates/main

- `main.py:Index()` -> templates/main/Index

- `main.py:Index(Mocha):index(self)` -> templates/main/Index/index.jade

- `main.py:Index(Mocha):about_us(self)` -> templates/main/Index/about_us.jade

- `main.py:Document()` -> templates/main/Document

- `main.py:Document(Mocha):index(self)` -> templates/main/Document/index.jade

- `main.py:Document(Mocha):get(self)` -> templates/main/Document/get.jade

Also, you may have noticed that we use `.jade` template instead of HTML, just for aesthetic, as it looks like python
on the templates side. But HTML can also be used.

`templates/main/Index/index.jade`

    .row
        .col-md-12.text-center
            h2= name
                small= version


Which will be translated into html

    <div class="row">
        <div class="col-md-12 text-center">
            <h2>Mocha <small>1.0</small></h2>
        </div>
    </div>

`templates/main/Document/index.jade`

    .row
        .col-md-12
            ul
            for doc in docs
                li: a(href=url_for('views.main.Document:get', id=doc.id))= doc.title

Will be translated into html

    <div class="row">
        <div class="col-md-12">
            <ul>
                <li><a href='/document/1'>This is a doc title</a></li>
            </ul>
        </div>
    </div>

---

## Layout

By default, layouts are placed in `application/templates/layouts`, and upon rendering Mocha will glue your view in the
layout.

The default layout is at: `application/templates/layouts/base.jade`

While you can have `extends` in your templates, Mocha makes it easy to bypass the repetitive tasks, so you can fully
focus on that one page you are working on.

    - import "contrib/components/html.html" as html with context
    - import "contrib/components/nav.jade" as nav with context
    - import "contrib/components/forms.html" as forms with context
    - import "contrib/components/widget.html" as widget with context

    !!! 5
    html(lang="en")
        head
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, initial-scale=1.0")
            + html.page_title()
            + html.page_description()
            + html.opengraph()
            + html.favicon("favicon.ico")
            + html.include_jquery()
            + html.include_bootstrap()
            + html.include_fontawesome()
            + html.include_bootswatch_theme('yeti')
            + html.include_css_file("commons.css")
            + html.include_css_file("styles.css")
            + html.include_js_file("app.js")
            + html.google_analytics()

        body

            .container
                - include __template__

            footer
                .container-fluid
                    .row
                        .col-md-12
                            .text-center.
                                &copy; {{ g.__YEAR__}} {{ config.APPLICATION_NAME }} {{ config.APPLICATION_VERSION }}


The most important part of the layout is `include __template__`. This where the view template will be injected.

There are much more stuff going on it the template, we can tackle them later.

---

## Static

Static hold your assets: js, css, images. They must be placed in `/application/static/`

Mocha uses `Flask-Assets` to manage your assets. Therefor `assets.yml` is a bundle collection, that allows you to
bundle css or js together.

`assets.yml`

    styles.css:
        output: "gen/styles.css"
        contents:
            - css/style.css

    app.js:
        output: "gen/app.js"
        contents:
            - js/app.js

And in your template you can call it

    + html.include_css_file("style.css")
    + html.include_js_file("app.js")


As a convenience, we include a  `package.json` if you want to download 3rd party scripts (js, css). You can either run
`npm install` in static directory, or run `mocha :install-assets`, which will install your assets in the `node_modules`

---

## Serve

Now we are done with our application, all we need to do is serve it.

    mocha :serve

The command above will run `brew.py`

`brew.py` is the entry point of the application.


    from mocha import Brew

    projects = {
        "main": [
            "main"
        ]
    }

    app = Brew(__name__, projects)


`projects` is a dict containing all the views to be used.

Let's say if we had the views: `main.py`, `account.py`, `music.py`, `books.py`

We could put them into one

    projects = {
        "main": [
            "main",
            "account",
            "music",
            "books"
        ]
    }

Upon serving the app, it would make all the endpoints available.

Let's say we want to run multiple application

    projects = {
        "main": [
            "main",
            "account"
        ],
        "library": [
            "music",
            "books"
        ]
    }

Now we have 2 applications: `main` and `library`

By default, Mocha will default to `main`

    mocha :serve

But to run `library`

    app=library mocha :serve

If two apps are running at the same time, you may need to specify a different port

    app=library mocha :serve --port 5001

