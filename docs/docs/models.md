

Location: `/application/models.py`

---

## Configuration

---

## db

---

## model

---

## Types

---

## Special Types

Beside the default SQLAlchemy column types,

[SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/en/latest/)

---

### DateTime

Alias to ArrowType, which provides way of saving **[Arrow](https://arrow.readthedocs.io/en/latest/)** objects into database.
It automatically changes Arrow objects to datetime objects on the way in and
datetime objects back to Arrow objects on the way out (when querying database).

*Example*

    from mocha import db

    class Article(db.Model):
        title = db.Column(db.String(255))
        published_at = db.Column(db.DateTime)


** Create **

    from mocha import utc_now, models

    models.Article.create(title='Hi', published_at=utc_now)

** Read **

    from mocha import models

    article = models.Article.get(1)

    article.created_at = article.created_at.replace(hours=-1)

    article.created_at.humanize()
    # 'an hour ago'

** Links **

[ArrowType](https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.arrow)

[Arrow](https://arrow.readthedocs.io/en/latest/)

[Arrow Tokens](https://arrow.readthedocs.io/en/latest/#tokens)


---

### StorageObjectType

StorageObjectType offers way of saving `Storage.Object` data structures to database.
It automatically changes Arrow objects to JSON objects on the way in and
`Storage.Object` objects back on the way out (when querying database).

*Example*

    from mocha import db

    class Article(db.Model):
        title = db.Column(db.String(255))
        published_at = db.Column(db.DateTime)
        image = db.Column(db.StorageObjectType)

** Create **

    from mocha import utc_now, models, upload_file

    image_file = "file/xyz.jpg"
    image = upload_file(image_file)

    models.Article.create(title='Hi', published_at=utc_now, image=image)

** Read **

    from mocha import models

    article = models.Article.get(1)

    article.image.url
    article.image.size
    article.image.download()


---

### EmailType

Provides a way for storing emails in a lower case.

*Example*

    from mocha import db

    class Article(db.Model):
        title = db.Column(db.String(255))
        published_at = db.Column(db.DateTime)
        email = db.Column(db.EmailType)


Link: [EmailType](https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.email)

---

### JSONType

JSONType offers way of saving JSON data structures to database.
On PostgreSQL the underlying implementation of this data type is ‘json’
while on other databases its simply ‘text’.

*Example*

    from mocha import db

    class Article(db.Model):
        title = db.Column(db.String(255))
        published_at = db.Column(db.DateTime)
        data = db.Column(db.JSONType)

** Create **

    from mocha import models, utc_now

    models.Article.create(title='Hello',
                          published_at=utc_now,
                          data={
                            "reference": "blah",
                            "tags": ["A", "B", "C"]
                          })

** Read **

    article = models.Article.get(1)

    article.data.get("reference")
    # blah

    article.data.get("tags")
    # ["A", "B", "C"]

    article.data.get("location", "Charlotte")
    # Charlotte

Link: [JSONType](https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.json)

---

## Generic Types


---

## SQLAlchemy-Utils Types

If you want to use the other types from
[SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html)

- ArrowType
- ChoiceType
- ColorType
- CountryType
- CurrencyType
- EmailType
- EncryptedType
- JSONType
- LocaleType
- LtreeType
- IPAddressType
- PasswordType
- PhoneNumberType
- ScalarListType
- TimezoneType
- TSVectorType
- URLType
- UUIDType
- WeekDaysType


