
## Overview 

Assembly allows you to send email from your application using SMTP or AWS SES.

Extension: 

- <a href="https://pythonhosted.org/Flask-Mail/" target="_blank">Flask-Mail</a>
- <a href="https://github.com/mardix/ses-mailer" target="_blank">SES-Mailer</a>


---

## Usage


### Set Sender

In the config file, set the MAIL_SENDER and MAIL_REPLY_TO.

```python
# config.py

#: MAIL_SENDER - The sender of the email by default
#: For SES, this email must be authorized
MAIL_SENDER = "me@myemail.com"

#: MAIL_REPLY_TO
#: The email to reply to by default
MAIL_REPLY_TO = "me@myemail.com"

```

---

### Import

```python
from assembly import send_mail
```

---


### Send Simple Email

To send basic email

```python
from assembly import send_mail

to = "user@email.com"
subject = "Welcome"
body = "Welcome to our site"

send_mail(to=to, subject=subject, body=body)

```

---

### Send Template Email

Having a template like this...

```sh
# welcome.txt

{% block subject %}
    Welcome {{name}} to our site 
{% endblock %}

{% block body %}
    Dear {{name}} this is the content of the message 

    Thank you very much for your visiting us
{% endblock %}
```

Send email with vars

```python
from assembly import send_mail

send_mail(to="x@y.com", 
        template="welcome.txt", 
        name="Mardix")
```

---

### Signal

The mail also emit a signal, which can be used to pre and post process information

```python
from assembly import send_mail

@send_mail.post
def process_email_sent(result, **kwargs):
    if result:
        print("Email sent successfully!")

```

---



## Templates

You can have pre-made templates to send email. It's easier to customize, 
and instead of having messages all over the place, you can now have a central place
to put the messages that will be sent.

The template must be a Jinja template, containing at least the following blocks:

- subject
- body
    

### Example of a template

Having a template file called `welcome.txt`, we will create two Jinja blocks: 'subject', 'body'.

We can also use `{{...}}` to assign variables.

```
# welcome.txt

{% block subject %}
    Welcome {{name}} to our site 
{% endblock %}

{% block body %}
    Dear {{name}} this is the content of the message 

    Thank you very much for your visiting us
{% endblock %}
```

### File Templates

File base templates is supported. Place the templates in a directory. 

By default, Assembly places them in `./_data/emails-templates/` 

Place your templates files in there. The files name will be used to retrieve the template.

inside of the config.py, 

```python
# config.py

MAIL_TEMPLATES_DIR = os.path.join(DATA_DIR, "mail-templates")
```

Structure of the templates directory

```
/_data/email-templates
    |
    |_ welcome.txt
    |
    |_ lost-password.txt
```

### Dictionary based templates

If you don't want to create files, you can dictionary based templates

```python

# config.py

MAIL_TEMPLATES_DICT = {
    "welcome.txt": """
        {% block subject %}I'm subject{% endblock %}
        {% block body %}How are you {{name}}?{% endblock %}
    """,
    "lost-password.txt": """
        {% block subject %}Lost Password{% endblock %}
        {% block body %}Hello {{ name }}. 
        Here's your new password: {{ new_password }} 
        {% endblock %}
    """,    
}
```
    
### Send Email

For either files or dictionary based templates:

```python
# welcome

send_mail(to="x@y.com", 
        template="welcome.txt", 
        name="Mardix")

# lost-password
send_mail(to="x@y.com", 
        template="lost-password.txt", 
        name="Mardix", 
        new_password="mynewpassword")
```
---

## Configuration

    # AWS SES
    # To use AWS SES to send email
    #:
    #: - To use the default AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    #: set MAIL_URI = "ses://"
    #: * To use a different credential:
    #: set MAIL_URI = "ses://{access_key}:{secret_key}@{region}"
    #:
    #: *** comment out if you are using SMTP instead
    MAIL_URI = "ses://"

    # SMTP
    #: If you are using SMTP, it will use Flask-Mail
    #: The uri for the smtp connection. It will use Flask-Mail
    #: format: smtp://USERNAME:PASSWORD@HOST:PORT
    #: with sll -> smtp+ssl://USERNAME:PASSWORD@HOST:PORT
    #: with ssl and tls -> smtp+ssl+tls://USERNAME:PASSWORD@HOST:PORT
    #:
    #: *** comment out if you are using SES instead
    # MAIL_URI = "smtp+ssl://{username}:{password}@{host}:{port}"\
    #    .format(username="", password="", host="smtp.gmail.com", port=465)

    #: MAIL_SENDER - The sender of the email by default
    #: For SES, this email must be authorized
    MAIL_SENDER = APPLICATION_ADMIN_EMAIL

    #: MAIL_REPLY_TO
    #: The email to reply to by default
    MAIL_REPLY_TO = APPLICATION_ADMIN_EMAIL

    #: MAIL_TEMPLATE
    #: a directory that contains the email template or a dict
    MAIL_TEMPLATE = os.path.join(DATA_DIR, "mail-templates")

    #: MAIL_TEMPLATE_CONTEXT
    #: a dict of all context to pass to the email by default
    MAIL_TEMPLATE_CONTEXT = {
        "site_name": APPLICATION_NAME,
        "site_url": APPLICATION_URL
    }


---

## API

For the core functionalities of Flask-Mail or SES-Mailer, import 
the extension that was set

```python
from assembly import ext
```

**mail.mail** is the object in the **ext** to use.

### For SES-Mailer

```python
from assembly import ext

ext.mail.mail.send(*args, **kw)

ext.mail.mail.send_template(*args, **kw)

```

### For Flask-Mail

```python
from assembly import ext

ext.mail.mail.send_message(*args, **kw)
```