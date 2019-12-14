

Assembly is a Pythonic Object-Oriented Web Framework built on Flask

---

### Requirements

- Python 3.6+
- Virtualenv

---

### Install

Install Assembly with `pip install assembly`

It is highly recommended to use a virtualenv, in this case let's
use VirtualenvWrapper (you can use any that is convenient for you)

```sh
mkvirtualenv my-first-app

workon my-first-app

pip install assembly

```

---

### Initialize

Initialize Assembly with `asm gen:init`

CD into the folder you intend to create the application, then run `asm gen:init`. 
This will setup the structure along with the necessary files to get started

```sh
cd app-dir

asm gen:init

```

### Launch first app

```sh
asm gen:serve
```
