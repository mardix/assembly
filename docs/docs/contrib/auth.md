### mocha.contrib.auth

**Auth** adds authentication to your application

It has 3 modules: `AuthLogin`, `AuthAccount`, `AuthAdmin`

**AuthLogin**: Creates a login page, including signup, lost-password, reset-password, logout.


**AuthAccount**: Creates an interface for the user to change their login and personal info.


**AuthAdmin**: Creates an admin interface to manage the users.


**Requirements**

After you install it (for the first time) in `INSTALLED_APPS`, run the
command `mocha setup-models`


**Installation**

    INSTALLED_APPS [
        {
            "app": "mocha.contrib.auth",
            "db": "application.models.db",
            "modules": {
                "login": {
                    "route": "/"
                },
                "account": {
                    "route": "/account/"
                },
                "admin": {
                    "route": "/admin/users"
                }
            },
            "options": {
                # for login and logout view
                "login_view": None,
                "logout_view": None,

                # permission
                "allow_signup": True,
                "allow_login": True,
                "allow_social_login": False,

                # Verification
                "verify_email": False,
                "verify_email_token_ttl": 60 * 24,
                "verify_email_template": "verify-email.txt",
                "verify_signup_email_template": "verify-signup-email.txt",

                # reset password
                "reset_password_method": "token",  # token or password
                "reset_password_token_ttl": 60,  # in minutes
                "reset_password_email_template": "reset-password.txt",

            }
        }

    ]

The `modules` contain the interface of what to use in *Auth*. If you don't
want to use certain module, just exclude it in the list.
**AuthLogin** is required in your modules.

ie:

**For Admin only**

    INSTALLED_APPS [
        {
            "app": "mocha.contrib.auth",
            "db": "application.models.db",
            "modules": {
                "login": {
                    "route": "/"
                },
                "admin": {
                    "route": "/admin/users"
                }
            },
            "options": {
                "allow_signup": False
            }
        }
    ]

**For User Account**

    INSTALLED_APPS [
        {
            "app": "mocha.contrib.auth",
            "db": "application.models.db",
            "modules": {
                "login": {
                    "route": "/"
                },
                "account": {
                    "route": "/account/"
                }
            }
        }
    ]


**Options**

    - `login_view`: the view to redirect to after login. By default it will go to `Index:index`
    - `logout_view`: The view to redirect to after logout. By defaut it will go to `Index:index`
    - `allow_signup`: A boolean to allow people to signup or not. Default `False`
    - `allow_login`: A boolean to allow people to login or not. Default `True`
    - `allow_social_login`: A boolean to allow people to use social login to signup/signin. NOT IMPLEMENTED YET
    - `verify_email`: A boolean to require user to verify email before they can continue signing up. Default `False`
    - `verify_email_token_ttl`: The time in minutes for the token to live. Beyond that it will not work
    - `verify_email_template`: A custom email template for email verification
    - `verify_signup_email_template`: A custom email for verification when signing up
    - `reset_password_method`: `token` or `email`. The type of password reset to use. A `password` will send a password reset. A `token` will send an email containing a token to click on
    - `reset_password_token_ttl`: The time in minutes for the token to live. Beyond that it will not work
    - `reset_password_email_template`: A custom email for password email template

## Auth.Decorators

**Auth** exposes some decorators to use in your application views endpoints

Import:

    import mocha.contrib.auth as auth


**`@auth.authenticated`** : Require authentication to access an endpoint

    class Index(Mocha):

        @auth.authenticated
        def secure_page(self):
            return


**`@auth.unauthenticated`** : When a whole class require authetication, but you want to exclude certain page

    class Index(Mocha):
        decorators = [auth.authenticated]

        def secure_page(self):
            return

        @auth.unauthenticated
        def non_secure_page(self):
            return

**`@auth.require_verified_email`** : To restrict endpoint access to only verified email users

    class Index(Mocha):

        @auth.require_verified_email
        def secure_page(self):
            return


**`@auth.logout_user`** : Upon accessing this endpoint will automatically log user out

    class Index(Mocha):

        @auth.logout_user
        def secure_page(self):
            return


**`@auth.accepts_admin_roles`** : Force an endpoint to accept users to have at least **ADMIN** roles

    class Index(Mocha):

        @auth.accepts_admin_roles
        def page(self):
            return


**`@auth.accepts_manager_roles`** : Force an endpoint to accept users to have at least **MANAGER** roles

    class Index(Mocha):

        @auth.accepts_manager_roles
        def page(self):
            return


**`@auth.accepts_contributor_roles`** : Force an endpoint to accept users to have at least **CONTRIBUTOR** roles

    class Index(Mocha):

        @auth.accepts_contributor_roles
        def page(self):
            return


**`@auth.accepts_moderator_roles`** : Force an endpoint to accept users to have at least **MODERATOR** roles

    class Index(Mocha):

        @auth.accepts_moderator_roles
        def page(self):
            return

**`@auth.accepts_roles(*roles)`** : Force an endpoint to accept users to have at one of the roles provided

    class Index(Mocha):

        @auth.accepts_roles('admin', 'manager', 'my-custom-role')
        def page(self):
            return


## Auth.Helpers

**Auth** also exposes some helpers functions.

Import:

    import mocha.contrib.auth as auth


**`auth.current_user`** returns the `AuthUser` object, containing the user info such as name, email, etc

**`auth.is_authenticated()`** return True if the `current_user` user is authenticated

**`auth.not_authenticated()`** return True if the `current_user` user is not authenticated

**`auth.get_user(id)`** returns `AuthUser` by id.

**`auth.authenticate_email(email, password)`** to Authenticate by email and password. returns `AuthUserLogin`


## Auth.signals

Auth come with some signals to help you do something before and/or after a user perform a task, such as login,
logout, signup etc.

**on_signup**

Pre Signup

    @auth.signals.on_signup.pre.connect
    def pre_signup(*a, *kw):
        pass

Post Signup

    @auth.signals.on_signup.post.connect
    def post_signup(sender, emitter, result, *a, *kw):
        pass

**on_login**

**on_logout**

**make_user_secure_token**

**get_user_from_secure_token**

**get_user_id_secure_token**

