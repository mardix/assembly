


**Mocha** also has some convenient filter to use in your template


## link_for

**`link_for`** creates an link tag base on endpoint

    {{ link_for("Index:about_us") }}

The code above would result into a link similar to this 

    <a href="/about-us">About Us</a>
    
Based on a view like this
    
    class Index(Mocha):
        
        @nav_menu("About Us")
        def about_us(self):
            pass


## date

**`date`** : To format a date based on the `DATE_FORMAT` in your config file

    {{ var_date | date }}
    
## date_time

**`date_time`** : To format a date based on the `DATE_TIME_FORMAT` in your config file

    {{ var_date | date_time }}
    
    
## format_datetime 

**`format_datetime(format)`** : To format a date 

    {{ var_date | format_datetime('MM/DD/YYYY') }}
    
    
## date_since

**`date_since`** :Show the date ago: show Today, Yesterday, July 27 (without year in same year), July 15 2014 

    {{ var_date | date_since }}
    
## time_since
 
**`time_since`** : To show the time ago: 3 min ago, 2 days ago, 1 year 7 days ago 

    {{ var_date | time_since }}
 
## img_src

**`img_src`**: Generate an <img src> tag

    {{ image_url | img_src }}

## oembed

**`oembed`**: To generate an oembed tag. Mocha will load the content via JS

    {{ url | oembed }}

## static

**`static`**: Generates a a url for static file

    <img src='{{ "file.jpg" | static }}'>
    
## slugify

**`slugify`** : 

    {{ varname | slugify }}

## markdown

**`markdown`** Transform a markdown text to safe html

    {{ var_markdown_content | markdown }}
    
## markdown_toc

**`markdown_toc`** From the markdown content, generate the table of content

    {{ var_markdown_content | markdown_toc }}

---

## Macros

## Forms

Forms expose forms fields.

    {% import "Mocha/macros/forms.html" as forms with context %}


## forms.get

### Create a GET form 

    To create a get form:

    {% call forms.get(request.endpoint) %}
    
    
    {% endcall %}

## forms.post

### Create a POST form 

    To create a post form, which will automatically include the `csrf_token` to prevent cross-site request forgery.
    
    {% call forms.post(request.endpoint) %}
    
    
    {% endcall %}
    
    
## forms.upload

### Create a UPLOAD form 

    To create a post form but with the ability to upload file, which will automatically include the `csrf_token` to prevent cross-site request forgery.
    
    {% call forms.upload(request.endpoint) %}
    
    
    {% endcall %}
    

## forms.input

    {{ form.input(label="Enter your name", name="name", value="", placeholder="Enter Name") }}

## forms.hidden

## forms.select

## forms.radio

## forms.checkbox

## forms.textarea

## forms.button

## forms.recaptcha

It creates the RECAPTCHA input 

    {{ forms.recaptcha() }}


## forms.examples

    {% call forms.post(request.endpoint) %}
    
        {{ forms.input(label="Name", name="name") }}
        {{ forms.input(label="City", name="city") }}
        {{ forms.radio(label="Favorite Colod", name="fav_color", options=[('blue', 'Blue'), ('red', 'Red')]) }}
        
        {{ forms.input(label="Upload Image", name="file", type="file") }}
        
        {{ form.button(type='submit') }}
    
    {% endcall %}
---
    
    
## Widget
    
Widget exposes some bootstrap widget 

    {% import "Mocha/macros/forms.widget" as widget with context %}


---


## Menu

    {% import "Mocha/macros/menu.html" as menu with context %}

