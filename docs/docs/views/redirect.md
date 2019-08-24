
As it is in Flask, `redirect` just redirects to another endpoint or url. However, Mocha put a little bit of
convenience in, by doing self reference or


## Import

    from mocha import redirect

## Usage

    class Index(Mocha):

        def index(self):
            pass

        def post(self):
            return redirect(self.index)


## With other views

If you will be redirecting in views that are not in the same module, yo will need to import the `views` object along
with redirect

    from mocha import redirect, views

#### Usage

    # views/main.py

    from mocha import redirect, views, request

    class Index(Mocha):

        @request.post
        def save_data():
            return redirect(views.account.Index.info)



-

    # views/account.py

    @request.route("/account")
    class Index(Mocha):

        def index(self):
            pass

        def info(self):
            pass