
## Overview

Flask natively provides `flash` and `get_flashed_messages` to set and get respectively feedback messages between requests to the user.

In the same context, it can be necessary to pass some data between request. Usually, to retain some data from one place to another, example from a form submission to a response page, `flash_data` and `get_flashed_data` will allow you to set data between request.

---
## Usage 

### flash_data

*version: 1.3.0*

Similar to `flask.flash`, `flash_data` allows to hold data between request. Only one flash_data can be set at a time. 

Along with the data you want to retain, an identifier can be passed along to make sure the section to retrieve the data 

`flash_data(data:Any, key:String|None)`



```python 

from assembly import Assembly, flash_data, get_flashed_data

class Index(Assembly):

  FLASHED_KEY = "index"
  
  def post(self):
    """
    This will set the data to be retrieved back
    """
    data = {}
    flash_data(data, self.FLASHED_KEY)
    return redirect(self.index)

  def index(self):
    flashed_data = get_flashed_data()
    if flashed_data[0] and flashed_data[1] == self.FLASHED_KEY:
      ...

```


### get_flashed_data

*version: 1.3.0*

Retrieve the data that was saved via `flash_data`. It will also remove clear the data. Subsequent request will no longer have the data previously maintain.

This method returns a tuple of two items, with the first being the data saved, and the second a identifier.

`get_flashed_data()` -> `tuple(data:Any, key:String|None)`

```python 

from assembly import Assembly, flash_data, get_flashed_data

class Index(Assembly):
  FLASHED_KEY = "index"
  
  def index(self):
    """
    Retrieve data from flashed
    It will 
    """
    flashed_data = get_flashed_data()
    if flashed_data[0] and flashed_data[1] === self.FLASHED_KEY:
      ...

  def post(self):
    data = {}
    flash_data(data, self.FLASHED_KEY)
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


