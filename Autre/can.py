glob = {}
glob["a"] = 2
b = 2

exec("a = a\nb = 3", glob)

print(glob["a"])
print(glob["b"])

f = lambda x: 2

