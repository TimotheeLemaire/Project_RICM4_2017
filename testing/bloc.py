class emps:
	def __init__(self) :
		self.l = []
	
	def __init__(self,nom) :
		self.l = []
		self.l.append(emp("e0",100))
	
	def add(self, emp):
		self.l.append(emp)
	
	def select(self,bloc=None):
		#employees.select(lambda e: e.salary > 10)
		#return reconue yes ie il va dans le bloc !!
		"""if bloc : 
			print( "reconue yes ")
		else : 
			print( "non :(")
		"""
		if not bloc : 
			print ("pas de test")
		else: 	
			for e in self.l :
				if bloc(e) :
					print(e.name)
					
	def deli(self,emp):
		for e in self.l :
			if e == emp : 
				self.l.remove(e)
		return self		
			
class emp:
	def __init__(self,nom,salaire):
		self.name = nom 
		self.salary = salaire  
		
e1 = emp("e1",5)
e2 = emp("e2",7)
e3 = emp("e3",12)
e4 = emp("e4",15)		
e5 = emp("e5",2)
e6= emp("e6",17)
employees = emps("yes")
employees.add(e1)
employees.add(e2)
employees.add(e3)
employees.add(e4)
employees.add(e5)
employees.add(e6)


employees.select(lambda e: e.salary > 10)
employees.select()

test = lambda e: e.salary > 10

c= 0

def f(e):	
	if e.salary < 10 :
		c += 1 
	return e.salary < 10
"""
print(test(e1))
print(test(e4))

print (e1==e1)
print (e1==e2)
"""
test_e = employees.deli(e3)

employees.select(f)

print(c)
#test_e.select(lambda e: e.salary > 10)
