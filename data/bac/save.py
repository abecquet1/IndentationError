def reverse(s):
	res = ""
	for c in s:
		res = c+res
	return res 

def palin(s):
	return s == reverse(s)
	coucou
