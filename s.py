
from collections import namedtuple

d = {
  "NAME": "Jones"
}
d_named = namedtuple('Struct', d.keys())(*d.values())

print(d_named.NAME)
d_named.NAME = "DARN"
print(d_named.NAME)