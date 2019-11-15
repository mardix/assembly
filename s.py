import re 

n = "_error_handler"
m = re.match(r"^_error_(\d+|handler)$", n)
print(m.groups())


# s = "__error_handler"
# print(s.lstrip("_"))