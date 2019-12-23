## Overview 

Assembly uses Flask-Login to provide user session management.

(From Flask-Login)

Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.

It will:

- Store the active user’s ID in the session, and let you log them in and out easily.
- Let you restrict views to logged-in (or logged-out) users.
- Handle the normally-tricky “remember me” functionality.
- Help protect your users’ sessions from being stolen by cookie thieves.


Extension: <a href="https://flask-login.readthedocs.io/en/latest/" target="_blank">Flask-Login</a>


---

## Setup

Assembly automatically set and exposes `login_manager`

---

## Usage


### login_manager

*version: 1.3.0*

---

### current_user

---

### login_user

---

### logout_user

---

### Config

```python

#--------- LOGIN_MANAGER ----------
# Flask-Login login_manager configuration
LOGIN_MANAGER = {
    #: The name of the view to redirect to when the user needs to log in.
    #: (This can be an absolute URL as well, if your authentication
    #: machinery is external to your application.)
    "login_view": None,

    #: The message to flash when a user is redirected to the login page.
    "login_message": "Please log in to access this page.",

    #: The message category to flash when a user is redirected to the login page.
    "login_message_category": "message",

    #: The name of the view to redirect to when the user needs to reauthenticate.
    "refresh_view": None,

    #: The message to flash when a user is redirected to the 'needs
    #: refresh' page.
    "needs_refresh_message": "Please reauthenticate to access this page.",

    #: The message category to flash when a user is redirected to the
    #: 'needs refresh' page.
    "needs_refresh_message_category": "message",
}


```