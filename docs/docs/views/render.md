

This module contains decorators that will alter the rendering of the view. It can change the response, or add
new elements on the page, ie: `json` will turn the endpoint into a json response, while `template` will change the
default template page to display, and `nav` will create a menu title.

---

### Import

    from mocha import render

---

## Response

By default, the responses will render normal HTML. But if you want to return
JSON, or XML data, the methods below will conveniently help you do that.

N.B.: The methods must return DICT for them to benefit from multiple response format


### json

It return a dict into JSON. Good for API endpoint.

    class Index(Mocha):

        @render.json
        def my_data(self):
            return {
                "name": "Mocha",
                "version": "xxx"
            }

### jsonp

It return a dict into JSON for JSONP.

    class Index(Mocha):

        @render.jsonp
        def my_data(self):
            return {
                "name": "Mocha",
                "version": "xxx"
            }


### xml

It return a dict into XML.

    class Index(Mocha):

        @render.xml
        def my_data(self):
            return {
                "name": "Mocha",
                "version": "xxx"
            }


### html

There is no decorator for HTML, as it will fall back to it if a view is not decorated
with `json` or `xml`



## Template

This decorator allows you to change the view template or layout

It can be applied on both class based or method based

Params:

**template(page, markup="jade")**

- page: the path of the new layout or template
- markup: the markup to use for all pages: `jade` or `html`


### Class based

This will change the default layout to another one.

    @render.template('/layouts/my-new-layouts.jade')
    class Index(Mocha):

        def index(self):
            return

        def hello(self):
            return


### Method based

By default the template for method is based on its name, to use a different
template, specify the full path

    class Index(Mocha):


        def index(self):
            return

        @render.template('/my-path/new-world.html', markup='html')
        def hello(self):
            return


## Navigation