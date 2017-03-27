class itera:
	def __init__(self):
		self.l=[1,12,3,45,5,60,7]
		self.dic= {"chemise":3, "pantalon":6, "tee shirt":7}
		
	def p__iter__(self) :
		for x in self.l:
			yield x
     		
	def __iter__(self,a) :
		for x in self.l:
			yield x
   
a=itera()

for e in a:
	print(e)
