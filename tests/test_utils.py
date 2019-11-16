
from flask import Flask
import functools
import assembly.utils as utils


def test_is_valid_email():
    assert utils.is_valid_email("youder.com") is False
    assert utils.is_valid_email("yo@uder.com") is True
    assert utils.is_valid_email("yo-uder@pp.com") is True
    assert utils.is_valid_email("yo.uder@pp.com") is True
    assert utils.is_valid_email("yo-uder@pp.co.com") is True

def test_is_valid_username():
    assert utils.is_valid_username("yo@uder.com") is False
    assert utils.is_valid_username("joe") is True
    assert utils.is_valid_username("joe-the-plumber") is True
    assert utils.is_valid_username("joe.dot") is True
    assert utils.is_valid_username("jess_one_tow") is True
    assert utils.is_valid_username("hello space") is False

def test_is_valid_password():
    """
    - min length is 6 and max length is 25
    - at least include a digit number,
    - at least a upcase and a lowcase letter
    - at least a special characters
    """
        
    assert utils.is_valid_password("abc") is False
    assert utils.is_valid_password("abcd") is False
    assert utils.is_valid_password("abcde") is False
    assert utils.is_valid_password("abcdef") is False
    assert utils.is_valid_password("abcdefhijklmnopqrstuvwxyz") is False
    assert utils.is_valid_password("!Password1") is True
    assert utils.is_valid_password("!PASSWORD1") is False
    assert utils.is_valid_password("!password1") is False
    assert utils.is_valid_password("PPassword1") is False
    

def test_gen_md5():
    assert len(utils.gen_md5("Hello")) == 32

def test_gen_uuid():
    assert len(utils.gen_uuid()) == 36

def test_gen_uuid_hex():
    assert len(utils.gen_uuid_hex()) == 32

def test_in_any_list():
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


def test_DotDict():
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

    dd = utils.DotDict(d)

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


def test_flatten_config_property():

    class Conf(object):

        CORS = {
            "NAME": "A",
            "B": "C",
            "D": "E"
        }

        AWS_ACCESS_KEY_ID = "NOT-CHANGED"
        AWS = {
            "ACCESS_KEY_ID": "SHOULD-NOT-CHANGE",
            "LOCATION": "ADDED"
        }

    app = Flask(__name__)
    app.testing = True
    app.config.from_object(Conf())

    utils.flatten_config_property("AWS", app.config)
    utils.flatten_config_property("CORS", app.config)

    assert app.config.get("AWS_ACCESS_KEY_ID") == "NOT-CHANGED"
    assert app.config.get("AWS_LOCATION") == "ADDED"
    assert app.config.get("CORS_NAME") == "A"


def test_prepare_view_response():

    data = {"A": "B"}
    result = utils.prepare_view_response(data)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], dict)
    assert result[1] is 200
    assert result[2] is None

    data = {"A": "B"}, 201
    result = utils.prepare_view_response(data)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], dict)
    assert result[1] is 201
    assert result[2] is None    

    data = {"A": "B"}, {"HEADERS": True}
    result = utils.prepare_view_response(data)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], dict)
    assert result[1] is None
    assert result[2] is not None     

    data = {"A": "B"}, 202, {"HEADERS": True}
    result = utils.prepare_view_response(data)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], dict)
    assert result[1] is 202
    assert result[2] is not None     