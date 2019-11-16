

Allows you to apply a route on a view class or a single method

---

## Import

    from mocha import request

---

## Class based

When applied to a view class, all methods will be prefixed with the toute

The following code will use the `/account/` route, and `/account/hello`


    @request.route("/account/")
    class Index(Mocha):

        def index(self):
            pass

        def hello(self):
            pass

---

## Method based

Method based route only applies the route to the method.

The code below will expose `/hello-world`. By default `Index` and `index` will
reference to the root, unless a route is applied

    class Index(Mocha):

        def index(self):
            pass

        @request.route("hello-world")
        def hello(self):
            pass

---

## Class and Method

You can combine both class and method based.

The code below will now be accessed at: `/account/`, `/account/hello-world`

    @request.route("/account/")
    class Index(Mocha):

        def index(self):
            pass

        @request.route("/hello-world")
        def hello(self):
            pass

