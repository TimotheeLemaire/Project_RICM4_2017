import yaml
from pprint import pprint
# some_file.py
import sys
sys.path.insert(0, '../dev/')
import resourceSet


def test_yaml():
	#Not sure how to parse yaml files into ResourceSet
	with open('resource_set2.yaml', 'r') as f:
		res = yaml.load(f)

#test ResourceSet
#******************
r = resourceSet.ResourceSet("toto")
r.append(resourceSet.Resource("node",None,"titi"))
tata = resourceSet.ResourceSet("tata")
tata.append(resourceSet.Resource("node",None,"tutu"))
r.append(tata)
#*****************


def test_select():

	r = resourceSet.ResourceSet("toto")
	r.append(resourceSet.Resource("node",None,"titi"))
	tata = resourceSet.ResourceSet("tata")
	tata.append(resourceSet.Resource("node",None,"tutu"))
	r.append(tata)

	#r1 = r.select('node',{'name':'tutu'})
	#r2 = r.select('node', (lambda x: x=='tutu')
	# assert(pprint(r1)==pprint(r2))
	
	# assert(r1 == r2)
	# assert(not(r1!=r2))


test_select()