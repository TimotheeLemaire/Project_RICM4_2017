

def f(b):
	l = [1,2,3,4]
	while l : 
		b( l.pop())

def length():
	count = 0  
	f(lambda x: count += 1)
	return count

#print(len(l))

print(length())
