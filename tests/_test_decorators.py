
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
