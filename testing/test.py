from execo import *

nbprocess = 10

set = []

for i in range(nbprocess):
	set.append(Process("./123Soleil "+str(i) ))

iter = set.__iter__()

print set

action = ParallelActions(set)

action.run()

for i in range(nbprocess):
	print set[i].stdout

