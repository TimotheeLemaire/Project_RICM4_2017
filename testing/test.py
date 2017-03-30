import yaml
from pprint import pprint
# some_file.py
import sys
sys.path.insert(0, '../dev/')
import resourceSet
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom



"""
class Foo(object):
    def __init__(self, s, l=None, d=None):
        self.s = s
        self.l1, self.l2 = l
        self.d = d

    def __str__(self):
        # print scalar, dict and list
        return('Foo({s}, {d}, [{l1}, {l2}])'.format(**self.__dict__))
"""
"""
def foo_constructor(loader, node):
    instance = Foo.__new__(Foo)
    yield instance
    state = loader.construct_mapping(node, deep=True)
    instance.__init__(**state)
yaml.dd_constructor('!Foo', foo_constructor)
"""

def test_yaml():
	#Not sure how to parse yaml files into ResourceSet
    #with open('resource_set1.yaml', 'r') as f:
    #with open('yaml.yaml', 'r') as f:
        #res = yaml.load(f)
    with open("yaml.yaml", 'r') as stream:
        try:
            print(yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)


#def resource __init__(self,typ, prop=None , name = None):
def res_from_xml(tree):
    #res = resourceSet.Resource()
    d_prop= dict()
    for child in tree :
        #print child.tag
        if child.tag == "properties":
            n_prop = child
        if child.tag =="type":
            type =  child.text
        
    for child in n_prop :
       d_prop[child.tag] = child.text
       if child.tag == "name":
           name = child.text
    
    res = resourceSet.Resource(type,d_prop,name)

    return res 

#RS __init__(self, name = None ):
def RS_from_xml(tree):
    resource_set = resourceSet.ResourceSet()
    
    for child in tree :
        if child.tag == "properties":
            n_prop = child
        elif child.tag == "resources":
            n_resources = child            
            
        elif child.tag =="type"  :
            resource_set.type = child.text
            
    for child in n_prop :
       resource_set.properties[child.tag] = child.text
       if child.tag == "name":
           resource_set.name = child.text
           
    for child in n_resources :
        if child.tag == "Resource":
            resource_set.append(res_from_xml(child))
        elif child.tag =="ResourceSet":
            resource_set.append(RS_from_xml(child))

    return resource_set

def test_xml():
    
    tree = ET.parse('xml/rs1.xml')
    root = tree.getroot()
    return (RS_from_xml(root))
    
    """
    res = res_from_xml(root)
    print res.properties
    print res.type"""
   
"""
r =test_xml()
print r
print "\n"

for i in resourceSet.ResourceSetIterator(r,"node"):
    print i
    
print "\nblanc\n"

for i in resourceSet.ResourceSetIterator(r,"resource_set"):
    print i
"""

def prettify(elem):
  # Return a pretty-printed XML string for the Element.
    
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def R_toxml(r):
    top = ET.Element('Resource')
    prop = ET.SubElement(top,"properties")
    
    for key,value in r.properties.items():
        c = ET.SubElement(prop, key)
        c.text = value
    
    n_t = ET.SubElement(top,"type")
    n_t.text = r.type
    
    return top 

def Rs_toxml(rs):
    top = ET.Element('ResourceSet')
    prop = ET.SubElement(top,"properties")
    
    for key,value in rs.properties.items():
        c = ET.SubElement(prop, key)
        c.text = value
    
    resources = []
    for res in rs.resources :
        if isinstance(res,resourceSet.ResourceSet):
            resources.append(Rs_toxml(res))
            
        elif isinstance(res,resourceSet.Resource):
            resources.append(R_toxml(res))
    
    top.extend(resources)    
    
    n_t = ET.SubElement(top,"type")
    n_t.text = rs.type
    
    return top

def xml_writer(r):
    return prettify(Rs_toxml(r))
        

#test ResourceSet
#******************
r = resourceSet.ResourceSet("toto")
tata = resourceSet.ResourceSet("tata")
tata.append(resourceSet.Resource("node",None,"tutu"))
tata.append(resourceSet.Resource("node",None,"tutu1"))
tata.append(resourceSet.Resource("node",None,"tutu2"))
tata.append(resourceSet.Resource("node",None,"tutu3"))
tyty = resourceSet.ResourceSet("tyty") 
tyty.append(resourceSet.Resource("node",None,"tete"))
tyty.append(resourceSet.Resource("node",None,"tete1"))
tyty.append(resourceSet.Resource("node",None,"tete2"))
tyty.append(resourceSet.Resource("node",None,"tete3"))
tyty.append(resourceSet.Resource("node",None,"tete4"))

tyty.append(tata)



r.append(resourceSet.Resource("node",None,"tl"))
r.append(resourceSet.Resource("node",None,"tp"))
r.append(resourceSet.Resource("node",None,"tu"))
r.append(tata) 

r.append(tata) 
r.append(resourceSet.Resource("node",None,"titi"))
r.append(resourceSet.Resource("node",None,"titi1"))
r.append(resourceSet.Resource("node",None,"titi3"))
r.append(tata) 
r.append(resourceSet.Resource("node",None,"titi4"))
r.append(resourceSet.Resource("node",None,"titi5"))
r.append(tyty)
#*****************

print (xml_writer(r) )
#test_yaml()


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

