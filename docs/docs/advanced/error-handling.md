
# Overview

Assembly allows you to handle your errors beautifully. 

### _error_handler

A special method `_error_handler` can be added in your view class to capture any HTTPException. 

A template with the name `error_handler.html` will be used.

Only one `_error_handler` can exist in the application. `_error_handler` will take precedence over 
the other error handlers. 

To use specific error handler, omit _error_handler instead use the `_error_$errorCode` for example 
`_error_404`


```python

# error/__init__.py

from assembly import Assembly, HTTPError

class Index(Assembly):

    def _error_handler(self, e):
        return {
            "e": e
        }

```

Template:

```html
<!-- error/templates/Index/error_handler.html -->

{% extends 'main/layouts/base.html' %}

{% block title %}Error {{ e.code }} {% endblock %}

{% block body %}
  <h1>Error: {{ e.code }}</h1>
  <h4>{{ e.description }}</h4>
{% endblock %}

```

### _error\_$errorCode

Only one `_error_handler` can exist in the application. `_error_handler` will take precedence over 
the other error handlers. 

To use specific error handler, omit _error_handler instead use the `_error_$errorCode` for example 
`_error_404`

$errorCode is valid HTTP Error Code. Invalid code will throw an error

A template with the name `error_$errorCode.html` will be used.


```python

# error/__init__.py

from assembly import Assembly, HTTPError

class Index(Assembly):

    def _error_404(self, e):
        return {
            "e": e
        }

    def _error_500(self, e):
        return {
            "e": e
        }
```

Template:

```html
<!-- error/templates/Index/error_404.html -->

{% extends 'main/layouts/base.html' %}

{% block title %}Error {{ e.code }} {% endblock %}

{% block body %}
  <h1>Error: {{ e.code }}</h1>
  <h4>{{ e.description }}</h4>
{% endblock %}


<!-- error/templates/Index/error_500.html -->

{% extends 'main/layouts/base.html' %}

{% block title %}Error {{ e.code }} {% endblock %}

{% block body %}
  <h1>Error: {{ e.code }}</h1>
  <h4>{{ e.description }}</h4>
{% endblock %}

```

---

## Error Method Usage

```python
from assembly import Assembly, HTTPError

class Index(Assembly):

    def index(self):
        raise HTTPError.Unauthorized()

    def trigger_404(self):
        raise HTTPError.NotFound()
```

### abort

`abort` can also be used to trigger error

```python
from assembly import Assembly, HTTPError

class Index(Assembly):

    def index(self):
        raise HTTPError.abort(401)

    def trigger_404(self):
        raise HTTPError.abort(404)
```

---

### Available Methods

#### BadRequest: 400

#### Unauthorized: 401

#### Forbidden: 403

#### NotFound: 404

#### MethodNotAllowed: 405

#### NotAcceptable: 406

#### RequestTimeout: 408

#### Conflict: 409

#### Gone: 410

#### LengthRequired: 411

#### PreconditionFailed: 412

#### RequestEntityTooLarge: 413

#### RequestURITooLarge: 414

#### UnsupportedMediaType: 415

#### RequestedRangeNotSatisfiable: 416

#### ExpectationFailed: 417

#### ImATeapot: 418

#### UnprocessableEntity: 422

#### Locked: 423

#### FailedDependency: 424

#### PreconditionRequired: 428

#### TooManyRequests: 429

#### RequestHeaderFieldsTooLarge: 431

#### UnavailableForLegalReasons: 451

#### InternalServerError: 500

#### NotImplemented: 501

#### BadGateway: 502

#### ServiceUnavailable: 503

#### GatewayTimeout: 504

#### HTTPVersionNotSupported: 505

#### ClientDisconnected

#### SecurityError






