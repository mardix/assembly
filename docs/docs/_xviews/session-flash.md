

## Session

Mocha natively uses Flask session, with the addition of having the ability to use as backend either: Redis, Memcache, S3, CloudStorage


### Config

    #: SESSION
    #: Flask-KVSession is used to save the user's session
    #: Set the SESSION_URL by using these examples below to set KVSession
    #: To use local session, just set SESSION_URL to None
    #:
    #: Redis: redis://username:password@host:6379/db
    #: S3: s3://username:password@s3.aws.amazon.com/bucket
    #: Google Storage: google_storage://username:password@cloud.google.com/bucket
    #: SQL: postgresql://username:password@host:3306/db
    #:      mysql+pysql://username:password@host:3306/db
    #:      sqlite://
    #: Memcached: memcache://host:port
    #:
    SESSION_URL = None


### Usage

    from mocha import session


---

## Flash

The Flash provides single-use string storage. It useful for implementing the Post/Redirect/Get pattern, or for transient
"Operation Successful!" or "Operation Failed!" messages

You can import the `flash` as is, but for convenience, we provided some special message pattern:

`flash_info`, `flash_success`, `flash_error` to indicate a info, success and error message respectively.


### Flash Message

#### Import

    from mocha import flash_info, flash_success, flash_error

#### Usage

    class Index(Mocha):

        def index(self):
            flash_info("You need to provide your account info")
            return

        def post(self):
            try:
                # do something
                flash_success('Account info saved successfully!')
            except Exception as ex:
                flash_error('An error occured while saving your info')

            return redirect(self.index)

---

### Flash Data

Same as flash message, you can also flash data


#### Import

    from mocha import flash_data, get_flash_data


#### Usage

    class Index(Mocha):

        def index(self):
            flash_data({"temp": 70})


        def get(self, id):
            temp = get_flash_data().get("temp")

