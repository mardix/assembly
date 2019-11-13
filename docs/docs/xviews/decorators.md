
# Decorators

Mocha exposes decorators to simplify your app development

---

## Render

---


---

## Cache

Flask-Caching is used for caching

### cache

    from mocha.ext import cache
    class Index(Mocha):

        @cache.cached(500)
        def my_cache_view(self):
            return

### memoize

---

## CSRF

All POST methods are required to receive `_csrf_token` from the application.

It it fails, the user will not be able to use it.


### exempt_csrf

In some cases you will want to bypass a POST method CSRF check, to do, we
have to exempt that method

    from mocha.ext import csrf
    import mocha.decorators as deco

    class Index(Mocha):

        @csrf.exempt
        @deco.accept_post
        def my_exempted_csrf_post(self):
            return

---

## nav_menu

**@nav_menu** creates a **navigation menu** for UI

    from mocha import nav_menu
    


## view_parser

**@view_parser**

    from mocha import view_parser

