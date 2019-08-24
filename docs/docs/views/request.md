
`request` is a proxy to `flask.request` object, with some additional decorators and attributes

---

### Import

    from mocha import request



---

## Methods

### get

`@request.get` set a view to accept only GET method

    class Index(Mocha):

        @request.get
        def index(self):
            # do something

---

### post

`@request.post` set  a view to accept only POST method

    class Index(Mocha):

        @request.post
        def index(self):
            # do something

---

### put


`@request.put` set  a view to accept only PUT method

    class Index(Mocha):

        @request.put
        def index(self):
            # do something



---

### delete


`@request.delete` set  a view to accept only DELETE method

    class Index(Mocha):

        @request.delete
        def index(self):
            # do something


---

### all

`@request.all` set a view to accept only ALL methods.

It will accept: GET, POST, PUT, DELETE, OPTIONS

    class Index(Mocha):

        @request.all
        def index(self):
            # do something


### Combine

An alternative to @all is to use all methods as

    class Index(Mocha):

        @request.get
        @request.post
        @request.put
        @request.delete
        @request.options
        def index(self):
            # do something

---

## Test Method

Usually if a view method accept more than one request method, it is best to test for the method

### IS_GET

`request.IS_GET` tests if the request method is GET

    class Index(Mocha):

        def index(self):
            if request.IS_GET:
                # do something

It is equivalent to `request.method == 'GET'`

---

### IS_POST

`request.IS_GET` tests if the request method is POST

    class Index(Mocha):

        def index(self):
            if request.IS_POST:
                # do something

It is equivalent to `request.method == 'POST'`

---

Same as above for PUT and DELETE

### IS_PUT

### IS_DELETE

---

## Args & Forms

<small>This is already part of Flask. It is added as a reference</small>

### args

`request.args.get` lets you get the query vars

    # http://127.0.0.1/?name=Mocha

    class Index(Mocha):

        def index(self):
            name = request.args.get("name")

### form

`request.form.get` lets you get the data that was sent in a post form

    class Index(Mocha):

        def index(self):
            name = request.form.get("name")

### getlist

`request.form.getlist` returns a list of all the items with the same name that was posted in a form


``` html
<input type='checkbox' name='options' value='apple'>
<input type='checkbox' name='options' value='orange'>
<input type='checkbox' name='options' value='grapes'>
```

Python

    class Index(Mocha):

        def index(self):
            my_options = request.form.getlist("options")

### files.get

`request.files.get` allow you to retrieve a file that was uploaded


HTML

``` html
<input type=file name="file">
```

Python

    class Index(Mocha):

        def index(self):
            file = request.files.get("file")


### files.getlist

`request.files.getlist` allow you to retrieve multiple files uploaded with the same name

HTML

``` html
<input type=file name="file">
<input type=file name="file">
<input type=file name="file">
```

Python

    class Index(Mocha):

        def index(self):
            files = request.files.getlist("file")


### Save uploaded file

Here's a snippet on how to upload a file.

    from mocha import request, upload_file

    class Index(Mocha):

        @request.post
        def upload_file(self):
            image_file = request.files.get("file")
            upload_file("image", file)

---


