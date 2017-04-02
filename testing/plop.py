class test: 
	#self.x = 12
	def __init__(self):
		self.x=1
	
	def plop(self,y):
		self.x = y
		
	
class test2:
	def __init__(self):
		self.y=12
#print(test.x )




a = test()
b = test2()
c= test2()
#print(type(a)==type(b))

#print(type(c)==type(b))

#print(c.__class__.__name__)


#print(a.x)
tmp = 100 
a.plop(tmp)

#print(a.x) 

a.x = 12
#print(a.x)

#print (c.__class__==b.__class__)

def test():
	try:
		raise StopIteration
	except StopIteration :
		print "yes"
	finally :
		print "omg"
	print "ole"
		
test()



