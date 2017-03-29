class itera:
		def __init__(self):
			self.l=[1,12,3,45,5,60,7]
			self.dic= {"chemise":3, "pantalon":6, "tee shirt":7}
			self.current=0

		def __getattribute__(self,l):
			if( l == "la"):
				print ("yo")
				return self.l[3]
			else :
				return self.l
		def __iter__(self) :
			# for x in self.l:
			# 	yield x
			return self

		def __len__(self):
			return len(self.l)


		def __delitem__(self,v):
			del( self.l[v] )
	     	
		def next(self):
			if self.current >= len(self.l):
				self.current = 0 
				raise StopIteration
				return None
			else:
				self.current += 1
				return self.l[self.current-1]

a=itera()
# print len(a)
# # print ("hello")
# # print (a.la)
# # 
# print "yayayayay"
# print( len (a.dic))


# for d in a:
# 	print (d)
# 	

# del a[1]

# print a.l


print a.dic["chemise"]

# print (a.next())
# print( a.next())
# print (a.next())
# print (a.next())
# print( a.next())
# print (a.next())
# print (a.next())
# print( a.next())
# print (a.next())
# print (a.next())
# print( a.next())
# print (a.next())
# print (a.next())
# print( a.next())
# print (a.next())

print ("huhuhuh")

for d in a: 
	print(( d))

# class yrange:
# 	def __init__(self, n):
# 		self.i = 0
# 		self.n = n

# 	def __iter__(self):
# 		return self

# 	def next(self):
# 		if self.i < self.n:
# 			i = self.i
# 			self.i += 1
# 			return i
# 		else:
# 			print "fin"
# 			self.i = 0 
# 			raise StopIteration()


# b= yrange(10)
# print b.next()
# print b.next()
# print "ffff"
# for c in b :
# 	print c

# for c in b :
# 	print c

