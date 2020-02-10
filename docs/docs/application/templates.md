
## Overview

Assembly uses Jinja2 as template language, and files are organized per Class and Methods name.

Extension: <a href="https://jinja.palletsprojects.com/en/2.10.x/templates/" target="_blank">Jinja2</a>

---

## Jinja2

Jinja2 is a powerful feature-packed template engine for Python. 

Visit **<a href="https://jinja.palletsprojects.com/en/2.10.x/templates/" target="_blank">Jinja2</a>** for a deeeper dive in Jinja2, which describes the syntax and semantics of the template engine and will be most useful as reference when creating Jinja templates.

Continue reading for integration with Assembly...


---

## Structure

Files are organized per Class and Methods name.  Each class name have corresponding **folder** with the same name, and every method have a corresponding **.html** with the same name inside of the folder.


Having a View like this...

```python
# views/admin.py

from assembly import Assembly

class Index(Assembly):
  def index(self):
    return 

  def login(self):
    return

class Articles(Assembly):
  def index(self):
    return 

  def all(self):
    return


class Movies(Assembly):
  def index(self):
    return 

  def guide(self):
    return

  def channels(self):
    return



```

will map to templates below

```
|- views/
    |- __init__.py
    |- admin.py
|- templates/
    |- admin/
      |- Index
          |- index.html
          |- login.html
      |- Articles
          |- index.html
          |- all.html
      |- Movies
          |- index.html
          |- guide.html            
          |- channels.html            
```

---

## Base Layout

---

## Data Context

With Assembly no need to use flask `render_template` to render a template. By returning the data as DICT, Assembly will properly use the right template and assign the context that was returned. 


```python

class Index(Assembly):
  def index(self):
    return {
      "name": "Assembly",
      "tag": "Awesomeness!",
      "items": ["Sky", "Brook", "Assembly", "Flask"]
    }
```

And In the HTML

```html

{% block body %}

  <h1>{{ name }}</h1>
  <h3>{{ tag }}</h1>

  <ul>
    {% for item in items %}
      <li>{{ item }}</li>
    {% endfor %}
  </ul>
{% endblock %}

```

---

## Template Inheritance

One important feature in template languages is template inheritance i.e a child template can inherit or extend a base template. This will allow you to define your template and a clear and concise way and avoid complexity.

You can use the `{% extends %}` and `{% block %}` tags to work with template inheritance.

The `{% extends %}` tag is used to specify the parent template that you want to extend from your current template and the `{% block %}` tag is used to define and override blocks in the base and child templates.

---

## Macros

We can implement DRY (Don't Repeat Yourself) principles in our templates by abstracting snippets of code that appear over and over into macros. If we're working on some HTML for our app's navigation, we might want to give a different class to the "active" link (i.e. the link to the current page). Without macros we'd end up with a block of if ... else statements that check each link to find the active one.

Macros provide a way to modularize that code; they work like functions. Let's look at how we'd mark the active link using a macro.

```html

{% from "macros.html" import nav_link with context %}

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{% block title %}{% endblock %}</title>
  </head>

  <body>
        
    <ul class="nav-list">
        {{ nav_link('home', 'Home') }}
        {{ nav_link('about', 'About') }}
        {{ nav_link('contact', 'Get in touch') }}
    </ul>
    
    <div class="container">
      {% block body %}{% endblock %}
    </div>

  </body>
  
```

And below is the definition of the macro in the macros.html

```html
<!-- templates/macros.html -->

{% macro nav_link(endpoint, text) %}
  {% if request.endpoint.endswith(endpoint) %}
      <li class="active"><a href="{{ url_for(endpoint) }}">{{text}}</a></li>
  {% else %}
      <li><a href="{{ url_for(endpoint) }}">{{text}}</a></li>
  {% endif %}
{% endmacro %}
```

---

## Filters

Jinja filters are functions that can be applied to the result of an expression in the 
`{{ ... }}` delimeters. It is applied before that result is printed to the template.

`{{ article.title|title }}`

In this code, the title filter will take `article.title` and return a title-cased version, which will then be printed to the template. This looks and works a lot like the UNIX practice of "piping" the output of one program to another.

We're going to define our filter in a module located at myapp/util/filters.py. This gives us a util package in which to put other miscellaneous modules.

```python
# /includes/filters.py

from assembly import app_context

def title(text):
    """Convert a string to all caps."""
    return text.uppercase()

def date_format(date_):
  if date_:
    return date_.format("YYYY-MM-DD")
  return ""
  
FILTERS = {
  "title": title,
  "date_format": date_format
}

@app
def filters(app):
  app.jinja_env.filters.update(FILTERS)

```

Once loaded, we can use it in our template

```
<h1>{{ article.title | title }}</h1>
<h2>{{ artitle.date | date_format }}
```

---


## URL_FOR


---

## CSRF_TOKEN

By default CSRF is enabled. In HTML, `csrf_token()` needs to be added for any POST forms.


```html
<input type='hidden' name="_csrf_token" value='{{ csrf_token() }}'>
```

Example:

```html
<h1>Upload</h1>
<form id="uploadbanner" action="/upload/" enctype="multipart/form-data" method="post">
    <input type='hidden' name="_csrf_token" value='{{ csrf_token() }}'>
    <input id="fileupload" name="file" type="file" />
    <input type="submit" value="Upload" id="submit" />
</form> 
```

Go to: **[CSRF](../advanced/csrf.md) **

---

## Extensions

### Assets

Via Flask-Assets, Assembly allows you to manage your static assets and use them in your template. By default, it will look into the `/static` directory for files.

Use `{% assets %}` tag to import any assets.


Extension: <a href="https://flask-assets.readthedocs.io/en/latest/" target="_blank">Flask-Assets</a>

#### Usage

In your template you include the files by using `{% assets 'path' %}`

```
    {% assets "css/styles.css" %}
        <link rel="stylesheet" href="{{ ASSET_URL }}">
    {% endassets %}
    
    {% assets "js/app.js" %}
      <script type="text/javascript" src="{{ ASSET_URL }}"></script>
    {% endassets %}
    
```


##### Bundle multiple files

```
{% assets "common/jquery.js", "site/base.js", "site/widgets.js" 
        output="gen/packed.js" %}
    <script type="text/javascript" src="{{ ASSET_URL }}"></script>
{% endassets %}

```

---

### Markdown

Markdown content is supported in Assembly. Markdown content will be converted to HTML.

 
#### Usage 

You can use Markdown in templates by including it `{% include "/path-to/file.md" %}` 
or via inline using `{% markdown %} content in markdown {% endmarkdown %}`

##### In View

```python
from assembly import ext

MKD = """
# Hello World

More things...
"""

my_mkd = ext.convert_markdown(MKD)

```

##### Include

Use the `{% include "/path-to/file.md" %}` to include and convert markdown to HTML in your template. 

*Supported files format:* `.md`, `.markdown`, `.mkd`, `.mkdown`

```html

{% block "body" %}

  <h1>Terms and Conditions</h1>
  
  <div>
    {% include "markdown-dir-under-templates/tos.md" %}
  </div>

{% endblock %}

```


##### Inline

Use `{% markdown %}` tag to convert inline Markdown content to HTML.

```html

{% block "body" %}

  {% markdown %}
  
    # Terms and Conditions

    ## Article 1

    ### Sub Article
      
  {% endmarkdown %}
  
{% endblock %}

```


---

### Inject Block

*version: 1.3.1*

This extension allows you to define placeholders where your blocks get rendered 
and at different places in your templates append to those blocks. 

This is especially useful for css and javascript. 

Your sub-templates can now define css and Javascript files 
to be included, and the css will be nicely put at the top and 
the Javascript to the bottom, just like you should. 

#### inject_block

`{% inject_block "$name" %}` injects the content that were defined in the sub templates.

##### Usage

`{% inject_block "css" %}` 


##### Example

```html
<!-- templates/layout/base.html -->

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    
    <title>{% block title %}{% endblock %}</title>

    {% assets "css/styles.css" %}
        <link rel="stylesheet" href="{{ ASSET_URL }}">
    {% endassets %}

    <!-- *** all the css from 'inject_into' will be included here -->
    {% inject_block "css" %}
    
  </head>

  <body>
    
    <header>
      {% block header %}{% endblock %}
    </header>
    
    <div class="container">
      {% block body %}{% endblock %}
    </div>

    <footer>
      {% block footer %}{% endblock %}
    </footer>

    {% assets "js/app.js" %}
      <script type="text/javascript" src="{{ ASSET_URL }}"></script>
    {% endassets %}
    
    <!-- *** all the js from 'inject_into' will be included here -->
    {% inject_block "js" %}
    
  </body>

```

#### inject_into

`{% inject_into "$name" %}` define the content that will be injected in a block.


##### Usage

```
  {% inject_into 'css' %}
    {% assets "css/main.css" %}
        <link rel="stylesheet" href="{{ ASSET_URL }}">
    {% endassets %}    
  {% endinject_into %}
```

##### Example

```html
<!-- templates/main/Index/index.html -->

{% extends 'layouts/base.html' %}

<!-- 
  inject_into 'css'
  add all CSS directives to be rendered in the {% inject_block 'css' %} 
-->
{% inject_into 'css' %}
    {% assets "css/main.css" %}
        <link rel="stylesheet" href="{{ ASSET_URL }}">
    {% endassets %}
{% endinject_into %}

<!-- 
  inject_into 'js'
  add all JS directives to be rendered in the {% inject_block 'js' %} 
-->
{% inject_into 'js' %}
  <script>
    console.log("Hello!")
  </script>
  
  {% assets "js/main.js" %}
    <script type="text/javascript" src="{{ ASSET_URL }}"></script>
  {% endassets %}  
  
{% endinject_into %}


{% block title %}Page Title{% endblock %}

{% block body %}
  The body of the page
{% endblock %}

```