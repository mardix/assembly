import re 

n = "_404_so"
m = re.match(r"^_(\d+)$", n)
print(m.groups())
