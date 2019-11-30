

## Overview

By default, Assembly will attempt to match a template with the view. Sometimes you may want to return JSON or cache the response. The `response` module provides some decorators to help with some response functionalities.

---

## Usage

```python
from assembly import response
```

### @json

Turn a response dict into a JSON

```python
class Index(Assembly):

    @response.json
    def api(self):
        return {
            "name": "Assembly"
        }
```

### @cache

Cache the response 

```python
class Index(Assembly):

    @response.json
    @response.cache(10)
    def api(self):
        return {
            "name": "Assembly"
        }
```

### @xml

Turn a response dict into an XML

```python
class Index(Assembly):

    @response.xml
    def api(self):
        return {
            "name": "Assembly"
        }
```

### @jsonp

### @template

Change the template that would be used by default to another one

```python
class Index(Assembly):

    @response.template("myOtherPackage/Index/api.html")
    def api(self):
        return {
            "name": "Assembly"
        }
```

### @headers

Add additional headers in the response

```python
class Index(Assembly):

    @response.headers({"X-COMMON": "something.2.4"})
    def api(self):
        return {
            "name": "Assembly"
        }
```

### @noindex

Add the no-index in the headers, hopefully, so search engines don't index the endpoint.

```python
class Index(Assembly):

    @response.noindex
    def api(self):
        return {
            "name": "Assembly"
        }
```
