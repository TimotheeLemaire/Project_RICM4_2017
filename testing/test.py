import yaml
from pprint import pprint
# some_file.py
import sys
sys.path.insert(0, '../dev/')
import resourceSet

class Foo(object):
    def __init__(self, s, l=None, d=None):
        self.s = s
        self.l1, self.l2 = l
        self.d = d

    def __str__(self):
        # print scalar, dict and list
        return('Foo({s}, {d}, [{l1}, {l2}])'.format(**self.__dict__))

def foo_constructor(loader, node):
    instance = Foo.__new__(Foo)
    yield instance
    state = loader.construct_mapping(node, deep=True)
    instance.__init__(**state)

yaml.add_constructor('!Foo', foo_constructor)

def test_yaml():
	#Not sure how to parse yaml files into ResourceSet
    #with open('resource_set2.yaml', 'r') as f:
    with open('yaml.yaml', 'r') as f:
        res = yaml.load(f)

        print res

#test ResourceSet
#******************
r = resourceSet.ResourceSet("toto")
r.append(resourceSet.Resource("node",None,"titi"))
tata = resourceSet.ResourceSet("tata")
tata.append(resourceSet.Resource("node",None,"tutu"))
r.append(tata)
#*****************


RI = resourceSet.ResourceSetIterator(r,"resource_set")

for i in r : 
    print  i
    break



#print r.resources

#print r.resources_files 

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


#test_select()

#test_yaml()