
## Overview

Request is a Proxy to Flask request with extra functionalities. For example it adds route decorator, cors decorator, etc.


## Usage

**Import**

```python
from assembly import request
```

### @route

```python
class Index(Assembly):

    # responds to -> /hello-world/
    @request.route("hello-world")
    def index(self):
        return
```

### @post

Restrict a method to only accepts POST request.

```python
class Index(Assembly):

    @request.post
    def index(self):
        return
```

### @get

Restrict a method to only accepts GET request.

```python
class Index(Assembly):

    @request.get
    def index(self):
        return
```

### @post_get

Restrict a method to only accepts POST and GET request.

```python
class Index(Assembly):

    @request.post_get
    def index(self):
        return
```


### @all

Restrict a method to only accepts all requests (POST, GET, PUT, DELETE, UPDATE, OPTIONS).

```python
class Index(Assembly):

    @request.all
    def index(self):
        return
```

### @put

Restrict a method to only accepts PUT request.

### @delete

Restrict a method to only accepts DELETE request.


### @cors

Make an endpoint CORS.  

```python
class Index(Assembly):

    @request.cors
    def index(self):
        return
```

### @csrf.exempt

To exempt CSRF on this endpoint.

```python
class Index(Assembly):

    @request.post
    @request.csrf.exempt
    def index(self):
        return
```

### get_auth_bearer

Get the authorization bearer, ie: JWT.

```python
class Index(Assembly):

    def index(self):
        auth_bearer = request.get_auth_bearer()
        return
```

### IS_GET

Test if a request is GET. Usually if one endpoint accepts multiple method

```python
class Index(Assembly):

    @request.post
    @request.get
    def index(self):
        if request.IS_GET:
            # do something
        return
```

### IS_POST

Test if a request is POST. Usually if one endpoint accepts multiple method

```python
class Index(Assembly):

    @request.post
    @request.get
    def index(self):
        if request.IS_POST:
            # do something
        return
```

### IS_PUT

Test if a request is PUT. Usually if one endpoint accepts multiple method

### IS_DELETE

Test if a request is DELETE. Usually if one endpoint accepts multiple method

### args

`request.args.get` lets you get the query vars

```
# http://127.0.0.1/?name=Assembly

request.args.get('name')
```

### form

`request.form.get` lets you get the data that was sent in a post form

### getlist

`request.form.getlist` returns a list of all the items with the same name that was posted in a form.

```html
# HTML
<input type='checkbox' name='options' value='apple'>
<input type='checkbox' name='options' value='orange'>
<input type='checkbox' name='options' value='grapes'>

# 
options = request.form.getlist("options")

```

### files.get

`request.files.get` allow you to retrieve a file that was uploaded

```html
# HTML
<input type=file name="file">

#py
file = request.files.get("file")

```

### files.getlist

`request.files.getlist` allow you to retrieve multiple files uploaded with the same name

```html
#HTML
<input type=file name="file">
<input type=file name="file">
<input type=file name="file">

#py
files = request.files.getlist('file')
```