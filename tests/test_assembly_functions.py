from flask import Flask
import functools
from assembly import assembly


def test__sanitize_module_name():
    from tests.module_test.main.__views__ import Test1
    assert assembly._sanitize_module_name(Test1.__module__) == "tests.module_test.main"


def test__register_models():
    class A:
      pass
    class B:
      pass

    assembly._register_models(A=A, B=B)
    assert assembly.models.A is A
    assert assembly.models.A is not B


def test__register_view():
    from tests.module_test.main.__views__ import Test1
    from tests.module_test.main2 import Test2
    assembly._register_view(Test1)
    assembly._register_view(Test2)
    assert hasattr(assembly.views.tests.module_test.main, 'Test1')
    assert hasattr(assembly.views.tests.module_test.main2, 'Test2')
