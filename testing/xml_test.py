import sys
sys.path.insert(0, '../dev/')
from resourceSet import *



r = ResourceSet("toto")
r.append(Resource("node",None,"titi"))
tata = ResourceSet("tata")
tata.append( Resource("node",None,"tutu"))
r.append(tata)


print (r)