def palin(s):
	for i in range(len(s)//2): 
		if s[i]!=s[-1-i]:
			return False
	return True
	
a = 1
def f():
	global a 
	a +=1
