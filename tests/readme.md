# Assembly Test

## Install

`pip install -r requirements-dev.txt`

---

## Run tests

To run the test, `cd tests`


#### Run all tests

`py.test`


#### Single test file

`py.test -q -s test_utils.py`


### Single test

`py.test -q -s test_utils.py::test_multi_replace_str`