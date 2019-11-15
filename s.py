import re 

n = "_xerror_handler"
m = re.match(r"^_error_(\d+|handler)$", n)
print(m)
#print(m.groups())


# s = "__error_handler"
# print(s.lstrip("_"))