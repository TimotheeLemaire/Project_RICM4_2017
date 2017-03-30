import yaml
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

        print(res)

#test ResourceSet
#******************

def resourceSet_test():
	r = resourceSet.ResourceSet("toto")
	r.append(resourceSet.Resource("node",None,"titi"))
	tata = resourceSet.ResourceSet("tata")
	tata.append(resourceSet.Resource("node",None,"tutu"))
	r.append(tata)
	return r

	# # for i in r.flatten().resources :
	# # 	print(i)
	# #*****************


	# # RI = resourceSet.ResourceSetIterator(r,"resource_set")
	# # for i in r : 
	# #     print (i)
	# #     break
	# # RI = resourceSet.ResourceSetIterator(r,"node")
	# # c = 0 
	# # for i in RI :
	# #     c +=1
	# #     print i
	# #     if c == 3 :
	# #         break

	# r.append(tata) 
	# r.append(resourceSet.Resource("node",None,"titi"))
	# r.append(resourceSet.Resource("node",None,"titi1"))
	# r.append(resourceSet.Resource("node",None,"titi3"))
	# r.append(tata) 
	# r.append(resourceSet.Resource("node",None,"titi4"))
	# r.append(resourceSet.Resource("node",None,"titi5"))
	# r.append(tyty)
#*****************

def test_select():

	r = resourceSet_test()

	r1 = r.select('node',({'name': 'tutu'}))
	r2 = r.select('node',block = (lambda x : x.name()=='tutu'))
	assert( r1 == r2 )
	assert( not (r1 != r2 ) )
	assert( r2 == r1 )
	assert( not (r2 != r1 ) )
	r1 = r.select('node',({'name': 'titi'}))
	r2 = r.select('node',block = (lambda x : x.name()=='tutu'))
	assert( r1 != r2 )
	assert( not (r1 == r2 ) )
	assert( r2 != r1 )
	assert( not (r2 == r1 ) )

	# print("r1 = :")
	# print(r1.type)
	# print(r1.properties)
	# print(r1.resources)
	# for j in r1.flatten().resources :
	#  	print(j)

	# print("r2 = :")
	# print(r2.type)
	# print(r2.properties)
	# print(r2.resources)
	# for i in r2.flatten().resources :
	# 	print(i)


def test_flatten() :

	r = resourceSet_test()

	r1 = r.select("node", {'name':'tutu'}).flatten('node')
	r2 = r.flatten('node').select('node', {'name':'tutu'})
	assert( r1 == r2 )
	assert( not (r1 != r2 ) )
	assert( r2 == r1 )
	assert( not (r2 != r1 ) )

def test_iterator() :
	r = resourceSet_test()

	it = resourceSet.ResourceSetIterator(r,'node')
	count = 0

	# for i in resourceSet.ResourceSetIterator(r,'node'):
	# 	count += 1
	while it.resource() :
		try :
			it.next()
		except StopIteration :
			break
		count += 1

	assert( count == 2)
	it = resourceSet.ResourceSetIterator(r,'node')
	assert(it.next() == r.resources[0])
	it.next()
	assert(it.resource() == r.resources[1].resources[0])
	it = resourceSet.ResourceSetIterator(r,'resource_set')
	assert(it.resource() == r.resources[1])

# TODO validity unsure and functionnality limited compared to expo/ruby try to use for statements instead
# def test_each

def test_uniq() :
	r = resourceSet_test()
	r.append(resourceSet.Resource('node',{'name':'titi'} ) )
	rs2 = r.select('node',{'name':'titi'} )
	count = 0
	for i in resourceSet.ResourceSetIterator(rs2,'node'):
		count += 1
	assert(count == 2)
	rs2 = r.uniq().select('node',{'name':'titi' } )
	count = 0
	for i in resourceSet.ResourceSetIterator(rs2,'node'):
		count += 1
	assert(count == 1)


# Test false, uncertitude about version of taktuk

# def test_make_taktuk_command() :
# 	r = resourceSet_test()
# 	r.properties['gateway'] = 'tyty'
# 	assert( r.make_taktuk_command("date") == " -m tyty -[ -m tutu -[ -m tutu downcast exec [ date ] -] -] -m tyty -[ -m titi downcast exec [ date ] -]")

test_select()
test_flatten()
test_iterator()
test_uniq()

#test_make_taktuk_command()

#test_yaml()