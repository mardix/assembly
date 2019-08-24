
import functools
import mocha.utils as utils


def test_encrypted_string():
    pw = "hello world"
    e = utils.encrypt_string(pw)
    v = utils.verify_encrypted_string(pw, e)
    assert v is True

def test_is_email_valid():
    assert utils.is_email_valid("youder.com") is False
    assert utils.is_email_valid("yo@uder.com") is True
    assert utils.is_email_valid("yo-uder@pp.com") is True
    assert utils.is_email_valid("yo.uder@pp.com") is True
    assert utils.is_email_valid("yo-uder@pp.co.com") is True

def test_is_username_valid():
    assert utils.is_username_valid("yo@uder.com") is False
    assert utils.is_username_valid("joe") is True
    assert utils.is_username_valid("joe-the-plumber") is True
    assert utils.is_username_valid("joe.dot") is True
    assert utils.is_username_valid("jess_one_tow") is True
    assert utils.is_username_valid("hello space") is False


def test_md5():
    assert len(utils.md5("Hello")) == 32

def _test_in_any_list():
    assert utils.in_any_list(["hello", "pops"], ["world", "cream"] ) is False
    assert utils.in_any_list(["hello", "pops"], ["world", "pops"] ) is True
    assert utils.in_any_list("The world of pops", ["world", "pops"] ) is True
    assert utils.in_any_list(["hello", "pops"], "This world has pops") is True
    assert utils.in_any_list("The world of pops", "in a world full of pop" ) is True

def text_chunk_list():
    l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
    c = utils.chunk_list(l, 2)
    assert len(c) == 7
    assert len(c[1]) == 2
    assert len(c[6]) == 1

def test_get_decorators_list():

    def deco1(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            return func(*args, **kwargs)
        return decorated_view

    def deco2(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            return func(*args, **kwargs)
        return decorated_view

    class Hi(object):

        @deco1
        @deco2
        def hello(self):
            return True

    k_hi = Hi()
    decos = utils.get_decorators_list(k_hi.hello)
    assert isinstance(decos, list)
    assert "deco1" in decos
    assert "deco2" in decos


def test_dict_dot():
    d = {
        "name": "Mardix",
        "location": {
            "street": "My Address",
            "city": "Charlotte",
            "state": "NC"
        },
        "family": {
            "wife": {
                "name": "Rara"
            },
            "kids": [
                {
                    "name": "Son#1",
                    "toys": [
                        "cars",
                        "paper",
                        "planes"
                    ]
                },
                {
                    "name": "Son#2"
                }
            ]
        }
    }

    dd = utils.dict_dot(d)

    assert dd.get("name") == "Mardix"
    assert dd["name"] == "Mardix"
    dd["name"] = "Jones"
    assert dd.get("name") == "Jones"
    assert dd.get("location.city") == "Charlotte"
    assert dd.get("location.zip_code") is None
    assert dd.get("location.area_code", 704) == 704
    assert isinstance(dd.get("family"), dict)
    assert dd.get("family.wife.name") == "Rara"
    assert dd.get("family.kids.0.name") == "Son#1"
    assert isinstance(dd.get("family.kids.0.toys"), list)
    assert dd.get("family.kids.0.toys.2") == "planes"
    assert dd.get("family.kids.1.name") == "Son#2"


def test_sign_jwt():
    secret = "abc"
    salt = "abc"
    d = "Hello World"
    s = utils.sign_jwt(d, secret_key=secret, expires_in=10, salt=salt)
    us = utils.unsign_jwt(s, secret_key=secret, salt=salt)
    assert us == d


def test_list_replace():
    string = "Hello Moto People"
    subject = ["Hello", "Moto"]
    repl = "OK"
    assert "Hello" not in utils.list_replace(subject, repl, string)
    assert "Moto" not in utils.list_replace(subject, repl, string)

def test_dict_replace():
    string = "Patriots are the champions"
    subject = {"Patriots": "Panthers", "champions": "winners"}
    assert "Panthers" in utils.dict_replace(subject, string)
    assert "winners" in utils.dict_replace(subject, string)
