
from flask import Flask
import harambe.decorators as decorators
import harambe.core as core

#===============================================================================
# EXTENDS
def test_extends():

    def plugin(view, **kwargs):
        class SubView(object):
            def inner(self):
                pass
        return SubView

    @decorators.plugin(plugin)
    class View(core.Harambe):
        pass

    i = View()
    assert hasattr(i, "inner") is True


#===============================================================================
# ROUTE
def test_route():
    def deco1():
        pass
    def deco2():
        pass

    @decorators.route("/a-section", decorators=[deco1, deco2])
    class A(core.Harambe):

        @decorators.route("home")
        def index(self):
            pass

    a = A()
    a.index()

    assert "/a-section" == a.base_route
    assert 2 == len(a.decorators)
    assert deco1 in a.decorators
    assert "home" == A.index._rule_cache["index"][0][0]


def test_methods():

    class A(core.Harambe):
        @decorators.methods("post")
        def path(self):
            pass

        @decorators.methods("post", "get", "put")
        def other(self):
            pass

        @decorators.get("/voila", endpoint="MyENDPOINTNAME")
        def tget(self):
            pass

        @decorators.post()
        def tpost(self):
            pass

        @decorators.put()
        def tput(self):
            pass

        @decorators.delete()
        def tdelete(self):
            pass


    a = A()
    a.path()
    a.other()
    a.tget()
    a.tpost()
    a.tput()
    a.tdelete()

    tget_rule_cache = a.tget.__dict__["_rule_cache"]["tget"][0]
    tget_rule = tget_rule_cache[0]
    tget_meth = tget_rule_cache[1]["methods"][0]

    assert "POST" in A.path._methods_cache
    assert "PUT" in A.other._methods_cache
    assert 3 == len(A.other._methods_cache)
    assert "GET" in tget_meth
    assert "/voila" == tget_rule


#===============================================================================
# MENU
def test_menu():
    menu = decorators.menu
    menu.clear()

    @menu("Hello World")
    class Hello(object):

        @menu("Index")
        def index(self):
            pass

        @menu("Page 2")
        def index2(self):
            pass

    @menu("Monster")
    class Monster(object):

        @menu("Home")
        def maggi(self):
            pass

    h = menu.get(Hello)
    assert len(menu.MENU) == 2

def test_menu_with_extends():
    menu = decorators.menu
    menu.clear()

    @menu("Hello World", group_name="admin")
    class Hello(object):

        @menu("Index")
        def index(self):
            pass

        @menu("Page 2")
        def index2(self):
            pass

    @menu("Monster", extends=Hello)
    class Monster(object):

        @menu("Home")
        def maggi(self):
            pass

    h = menu.get(Hello)
    assert h["kwargs"]["group_name"] == "admin"
    assert len(h["sub_menu"]) == 2

def test_menu_with_advanced_extends():
    menu = decorators.menu
    menu.clear()

    @menu("Hello World", group_name="admin")
    class Hello(object):

        @menu("Index")
        def index(self):
            pass

        @menu("Page 2")
        def index2(self):
            pass

    @menu("Monster", extends=Hello)
    class Monster(object):

        @menu("Home", extends=Hello)
        def maggi(self):
            pass

    h = menu.get(Hello)
    assert len(h["sub_menu"]) == 3

def test_menu_render():
    menu = decorators.menu
    menu.clear()
    app = Flask(__name__)
    app.testing = True

    @menu("Hello World", group_name="admin")
    class Hello(object):

        @menu("Index")
        def index(self):
            pass

        @menu("Page 2")
        def index2(self):
            pass

    @menu("Monster")
    class Monster(object):

        @menu("Home")
        def maggi(self):
            pass

    with app.test_client() as c:
        c.get("/")
        assert len(menu.render()) == 2

#===============================================================================
# LAYOUT

def test_template():
    @decorators.template("layout.html", name="Jone")
    class A(core.Harambe):

        @decorators.template("index.html", version=1)
        def index(self):
            return {}

        @decorators.template("index2.html", layout="NewLayout.html")
        def index2(self):
            return {}

        @decorators.template("index2.html", layout="NewLayout.html")
        def index3(self):
            return {
                "template_": "other.html",
                "layout_": "other-layout.html"
            }
    a = A()
    ai1 = a.index()
    ai2 = a.index2()
    ai3 = a.index3()

    assert "layout.html" == a._template_extends__.get("layout")
    assert "layout.html" == a.base_layout
    assert "index.html" == ai1["template_"]
    assert "index2.html" == ai2["template_"]
    assert "NewLayout.html" == ai2["layout_"]
    assert "other.html" == ai3["template_"]
    assert "other-layout.html" == ai3["layout_"]
    assert 1 == ai1["version"]

def test_template_with_extension():

    @decorators.template(brand_name="My Admin Zone")
    class A(core.Harambe):
        pass

    @decorators.template("Juice/admin/layout.html", extends=A)
    class B(core.Harambe):
        pass

    @decorators.template(extends=B, brand_name="Other")
    class C(core.Harambe):
        pass

    a = A()
    b = B()
    c = C()

    assert "layout.html" in a._template_extends__.get("layout")
    assert "Juice/admin/layout.html" in b._template_extends__.get("layout")
    assert "My Admin Zone" in b._template_extends__.get("brand_name")
    assert "Other" in c._template_extends__.get("brand_name")

#===============================================================================
# RENDER AS

def test_render_json():
    import json

    app = Flask(__name__)
    app.testing = True

    @app.route("/")
    @decorators.render_json
    def index():
        return {"test": "ok"}

    with app.test_client() as c:
        assert {"test": "ok"} == json.loads(c.get("/").data)

def test_render_xml():

    app = Flask(__name__)
    app.testing = True

    @app.route("/")
    @decorators.render_xml
    def index():
        return {"test": "ok"}

    with app.test_client() as c:
        data = c.get("/").data
        assert '<?xml version="1.0"' in data
