class test:
	def __init__(self):
		self.l =[1,12,3,45,5,60,7]

	def __getitem__(self,indice):
		if isinstance(indice,str) :
			return self.l[0]
		else :
			return self.l[-indice]


t = test()

print( t["zero"])

print(t[1])