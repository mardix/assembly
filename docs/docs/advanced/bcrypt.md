`bcrypt` from the `passlib` library is used to hash and verify password.


#### Import

    from mocha import bcrypt

#### Hash password

Hash a password for storage

    my_string_pass = "mypass123"
    my_hash = bcrypt.hash(my_string_pass)

#### Verify password

Verify a password by using the string provided to hash, and the hash that was created previously. It returns a bool.

    bcrypt.verify(my_string_pass, my_hash)


#### Config

`bcrypt` can be used with no configuration as it will fall back to its default. But if you want you can have the following
config

    BCRYPT_SALT = ""

    BCRYPT_ROUNDS = 12

    BCRYPT_INDENT = ""

