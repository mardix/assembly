
# Templates Macros

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

