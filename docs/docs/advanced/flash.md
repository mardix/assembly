
## Overview

Flask natively provides `flash` and `get_flashed_messages` to set and get respectively feedback messages between requests to the user.

In the same context, it can be necessary to pass some data between request. Usually, to retain some data from one place to another, example from a form submission to a response page, `flash_data` and `get_flashed_data` will allow you to set data between request.

---
## Usage 

### flash_data

*version: 1.3.0*

Similar to `flask.flash`, `flash_data` allows to hold data between request. Only one flash_data can be set at a time. 

```python 

from assembly import Assembly, flash_data, get_flashed_data

class Index(Assembly):

  def post(self):
    """
    This will set the data to be retrieved back
    """
    data = {}
    flash_data(data)
    return redirect(self.index)

  def index(self):
    flashed_data = get_flashed_data()
    if flashed_data:
      ...

```


### get_flashed_data

*version: 1.3.0*

Retrieve the data that was saved via `flash_data`. It will also remove

```python 

from assembly import Assembly, flash_data, get_flashed_data

class Index(Assembly):

  def index(self):
    """
    Retrieve data from flashed
    It will 
    """
    flashed_data = get_flashed_data()
    if flashed_data:
      ...

  def post(self):
    data = {}
    flash_data(data)
    return redirect(self.index)

```


### flash

*Flask native*

`flash` to set a message

```python
from assembly import Assembly
from flask import flash

class Index(Assembly):
  def index(self):
    flash("Welcome!")

  def with_category(self):
    flash("Hello", "info")
    flash("Something wrong!", "error")
    flash("You are about to do something bad", "warning")
    flash("Congratulations", "success")

```

### get_flashed_messages

*Flask native*

`get_flashed_messages` to retrieved the messages. Usually in the template

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class=flashes>
    {% for category, message in messages %}
      <li class="{{ category }}">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

```

Filter Messages

```html

{% with errors = get_flashed_messages(category_filter=["error"]) %}
{% if errors %}
<div class="alert-message block-message error">
  <a class="close" href="#">×</a>
  <ul>
    {%- for msg in errors %}
    <li>{{ msg }}</li>
    {% endfor -%}
  </ul>
</div>
{% endif %}
{% endwith %}

```


