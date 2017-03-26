class t:
	def __init__(self):
		self.bidon = 10 ; 
		
		
tmp = t() 
tmp2=t()
print(tmp.__class__.__name__)


print(type(tmp) == type(tmp2))

print(tmp.__class__ == tmp2.__class__)

print(tmp.__class__.__name__ == tmp2.__class__.__name__)


#print(tmp.__class__.__name__ == t )

l= []
print(isinstance(l,list ))
#print(isinstance(tmp,t ))



g = lambda e : e+e
print('callable:')
#print(g(10))
#print(type(g))
print (callable(g))
#print(isinstance(g,function ))
