## Contact Page

### mocha.contrib.views.contact_page

Adds a contact page interface.

**Installation**

    CONTACT = ("mocha.contrib.views.contact_page", {
        "route": "/contact/",
        "nav": {
            "title": "Contact",
            "order": 100
        }
        "recipients": "recipients@email.com",
        "success_message": "The message to show when the email is sent successfully",
        "title": "Contact Us",
        "return_to": "/"
    })

    INSTALLED_APPS: [
        CONTACT
    ]

**Options**

    - `recipients`: The email address to send the message to

    - `return_to`: The view endpoint or url to return to

    - `title`: The page title

    - `success_message`: The message to show when the email is sent successfully

---