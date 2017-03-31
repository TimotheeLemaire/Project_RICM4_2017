import copy
import yaml
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom


"""
    ``ResourceSet`` module
    ======================
 
    Used to gather resources into an object with several usefull functions 
 
    :Example:
 
    >>> from resourceSet import *
    >>> resource_set = parser_xml("resourceSet.xml")
    >>> for i in resource_set :
    >>>     print i 
    node1
    node2
    node3
    node4

 
    important features :
    -------------------
 
    Resource_set is made iterable by using the class ResourceSetIterator(resource_set,"type ask")
    resource_set behave like a usual python list
    Most of the list function are available : 
        del 
        resourceSet[indice]
        resourceSet.append(..)
        len(resourceSet)

    Every functions embodied documentation, and to acces documention simply call help(function ) in python shell
 
 
"""


#A Resource maps a computational resource to an object which keeps 
#Certains characteritics such as type, name, gateway.
class Resource(object):
    """
    Class Resource 

        Attributes:
            type         type of the resource of type string
            properties   properties of the resources of type dict

    """

    def __init__(self,typ, prop=None , name = None):
        """ Creates a new Resource Object.


            :param typ: The first number to add
            :param prop:  object property
            :param name: String name
            :type typ: string
            :type prop: dict
            :type name : string
            :return: Resource Object
            :rtype: Resource

            :Example:

            >>> r = Resource("node",name="toto")
            <resourceSet.Reousrce object at .... >
        """
        self.type = typ #type of the resource
        self.properties = dict()  #properties of the resources
        if prop : 
            self.properties = prop

        if name :
            self.properties["name"] = name 


    def name(self) :
        """ Return the name of the resource.

            :return: the name of the resource
            :rtype: str


        """
        return self.properties["name"]

    def __str__(self) :
        """ Return the name of the resource.

            :return: the name of the resource
            :rtype: str

            call with str(obj)

             :Example:

            >>> str(r)
            toto
        """
        return self.properties["name"]        

    def name_equal(self,name):
        """ Sets the name of the resource.

            :param name: String name
            :type name : string
        """
        self.properties["name"] = name
        return self
    

    def ssh_user(self):
        """ Return propertie ssh_user.

            :return: propertie ssh_user.
        """
        return self.properties["ssh_user"]
    
    
    def gw_ssh_user(self):
        """ Return propertie gw_ssh_user.

            :return: properties gw_ssh_user.
        """
        return self.properties["gw_ssh_user"]
    

    def corresponds(self, props ):
        """ check if a resource corresponds to the props
           
            Also test whenever a value of the properties are callable: test the callable value with key as an argument


            :param prop:  object property
            :type prop: dict



            :return: True if the resource have the same properties than the parameters 
            :rtype: Boolean
        """        
        for key,value in props.items():
            if callable(value) :
                if not value(self.properties[key]):
                    return False
            else :
                if (self.properties[key] != value):
                    return False
        return True  # return props == self.preperties ? 

    
  
    #Creates a copy of the resource object.
    def copy(self):
        result = Resource(self.type)
        result.properties =  self.properties 
        return result
    

    #Equality, Two Resource objects are equal if they have the 
    #same type and the same properties as well.
    def __eq__( self,res ): 
        return self.type == res.type and self.properties == res.properties
    

    #Returns true if self and other are the same object.
    def eql( self,res ):
        if self.type == res.type and self.__class__ == res.__class__:
            for key,value in self.properties.items():
                if(res.properties[key] != value):
                    return False 
            return True 
        else :
            return False

    #Returns the name of the gateway
    def gateway(self):
        if self.properties["gateway"]:
            return self.properties["gateway"] 
        return "localhost"
    

    def gateway_equal(self,host):
      self.properties["gateway"] = host
      #return self
    
    #alias gw gateway
    gw = gateway


    def job(self):
        if self.properties["id"]:
            return self.properties["id"] 
        return 0


    #Use to make the list of machines for
    #the taktuk command
    def make_taktuk_command(self,cmd) :
        return " -m " +self.name()
    


#class ResourceSetIterator

"""********************************
classe resourceSet  : 
    

***********************************"""
class ResourceSet(Resource):
    #attr_accessor :resources
    
    def __init__(self, name = None ):
            super(ResourceSet, self).__init__("resource_set", None, name )
            self.resources = []
            self.resource_files = dict()
        

    #Creates a copy of the ResourceSet Object
    def copy(self):
            result = ResourceSet()
            result.properties = self.properties 
            for resource in self.resources :
                result.resources.append(copy.deepcopy(resource))

            return result
        

    #Add a Resource object to the ResourceSet
    #On devrait peut etre le renommer en append ?
    def append(self, resource ):
      self.resources.append( resource )
      return self
        

    # Return the first element which is an object of the Resource Class
    def first (self, type=None ):
        for resource in self.resources:
            if (resource.type == type) :
                return resource
            elif isinstance(resource,ResourceSet):
                res = resource.first( type )
                if (res) :
                    return res 
            elif (not type) :
                return resource
        return None
        

    def select_resource(self, props ):
        for resource in self.resources:
            if resource.corresponds( props ) :
                return resource


    def select(self, type=None, props=None , block=None):
        set = ResourceSet()
        if not block :
            set.properties = self.properties 
            for resource in self.resources :
                if not type or resource.type == type :
                    if resource.corresponds( props ) :
                        set.resources.append( resource.copy() )
                elif type != "resource_set" and isinstance(resource,ResourceSet) :
                    set.resources.append( resource.select( type, props ) )
        else :
            set.properties = self.properties 
            for resource in self.resources :
                if not type or resource.type == type :
                    if block( resource ) :
                        set.resources.append( resource.copy() )
                        
                elif type != "resource_set" and isinstance(resource,ResourceSet) :
                    set.resources.append( resource.select( type, props , block) )
        return set
    

    def delete_first(self,resource):
        for i in range(len(self.resources)) :
            if self.resources[i] == resource :
                self.resources.pop(i)
                return resource
            elif isinstance(self.resources[i],ResourceSet) :
                if self.resources[i].delete_first( resource ) :
                    return resource
        return None
        

    def delete_first_if(self,block=None):
            for i in range(len(self.resources)) :
                if block(self.resources[i]) :
                    return self.resources.pop(i)
                elif isinstance(self.resources[i],ResourceSet) :
                    res = self.resources[i].delete_first_if( block )
                    if (res) :
                        return res
            return None
        
    #del ? __del__
    def delate(self,resource):
            res = None
            for i in range(len(self.resources)) :
                if self.resources[i] == resource :
                    self.resources.pop(i)
                    res = resource
                elif isinstance(self.resources[i],ResourceSet) :
                    #if self.resources[i].delete_all( resource ) :
                    if self.resources[i].delete( resource ) :
                        res = resource
            return res
        

    def delete_if(self,block=None):
        for i in range(len(self.resources)) :
            if block(self.resources[i]) :
                self.resources.pop(i)
            elif isinstance(self.resources[i],ResourceSet) :
                self.resources[i].delete_if( block )
        return self
        

    #Puts all the resource hierarchy into one ResourceSet.
    #The type can be either node or resource_set.
    def flatten(self, type = None ):
        set = ResourceSet()
        for resource in self.resources:
            if not type or resource.type == type :
                set.resources.append( resource.copy() )
                if isinstance(resource,ResourceSet) :
                    del set.resources[-1].resources[:]
            if isinstance(resource,ResourceSet) :
                set.resources.extend( resource.flatten(type).resources )
        return set
    

    # def flatten! (self,type = None ):
    def flatten_not (self,type = None ):
        set = self.flatten(type)
        self.resources = set.resources 
        return self
    


        # alias all flatten

    #Creates groups of increasing size based on
    #the slice_step paramater. This goes until the 
    #size of the ResourceSet.
    def each_slice( self,type = None, slice_step = 1, block=None):
        i = 1
        number = 0
        while True :
            resource_set = ResourceSet()
            it = ResourceSetIterator(self, type)
            #----is slice_step a block? if we call from
            #----each_slice_power2 : yes
            
            #if isinstance(slice_step,Proc) :
            if callable(slice_step):
                number = slice_step(i)

            elif isinstance(slice_step,list) :
                number = slice_step.shift.to_i
            else :
                number += slice_step
            if (number == 0):
                return None 
            for j in range(1,number) :
                resource = it.resource()
                if resource :
                        resource_set.resources.append( resource )
                else :
                    return None
                
                it.next()
            
            block( resource_set );
            i += 1
                 
        

    #Invokes the block for each set of power of two resources.
    def each_slice_power2(self, type = None, block=None ):
        self.each_slice( type, lambda i :  i*i , block )
        

    def each_slice_double( self,type = None, block=None ):
        self.each_slice( type, lambda i :  2**i , block )
    
    ## Fix Me  is the type really important , or were are going to deal always with nodes
    def each_slice_array( self,slices=1, block=None):
        self.each_slice( None,slices, block)
        

    #Calls block once for each element in self, depending on the type of resource.
    #if the type is :resource_set, it is going to iterate over the several resoruce sets defined.
    #:node it is the default type which iterates over all the resources defined in the resource set.
    #
    # ********************************
    #  deprecated 
    #  ********************************
    #   
    #def each( self,type = None, block=None ):
    #     it = ResourceSetIterator(self, type)
    #     while it.resource() :
    #         block( it.resource() )
    #         it.next()
    #         
    #         ************************************
            
    def each( self,type = None, block=None ):
        for resource in ResourceSetIterator(self, type):
            block( resource )            
        
    """TODO !!! """
    # Returns the number of resources in the ResourceSet
    # self.return [Integer] the number of resources
    """
    def length(self):
        count=0
        self.each("node",lambda count : count+=1) # impossible d'incrementer en fonction lambda
        return count
    """
# |      x.__getattribute__('name') <==> x.name
        #__getattribute('resource')
    def __len__(self):
        count = 0 
        for resource in ResourceSetIterator(self, "node"):
            count +=1
        return count

    # Returns a subset of the ResourceSet.
    # self.note It can be used with a range as a parameter.
        # self.param [Range] index  Returns a subset specified by the range.
        # self.param [String] index Returns a subset which is belongs to the same cluster.
        # self.param [Integer] index    Returns just one resource.
    # self.return [ResourceSet]     a ResourceSet object
    # self.example 
    #   all[1..6] extract resources from 1 to 6
    #   all["lyon"] extract the resources form lyon cluster
    #   all[0]  return just one resource.
    def __getitem__( self,index ):
        count=0
        resource_set = ResourceSet()
        #it = ResourceSetIterator()
        it = ResourceSetIterator(self,"node")
        if isinstance(index,list) : #Range
            for node in ResourceSetIterator(self,"node") :
                resource=it.resource()
                if resource :
                    if (count >= index[0] ) and (count <= index.max) :
                        resource_set.resources.apppend( resource )
                        count+=1
                        it.next()
            resource_set.properties=copy.deepcopy(self.properties)
            return resource_set

        if isinstance(index,str) :
            it = ResourceSetIterator(self,"resource_set")
            for resource in ResourceSetIterator(self,"resource_set") :
                if resource.properties["alias"] == index :
                    return resource

          #For this case a number is passed and we return a resource Object
              
        
        #TODO verifie la validite de ce code il est bizarre 
        for resource in ResourceSetIterator(self,"node"): 
            #resource = it.resource()
            #if resource :
            if count==index :
                #resource_set.resources.push( resource )
                return resource
            count+=1
            #it.next()
        
        raise StopIteration
        return  

        
    

    # Returns a resouce or an array of resources.
    # self.return [Resource] a resource or array of resources
    def to_resource(self)  :
        if len(self) == 1 :
            #la boucle est pas necessaire mais cela est simmilaire au ruby vec un each
            for resource in ResourceSetIterator(self,"node"):
                return resource
        else :
            resource_list = []
            for resource in ResourceSetIterator(self,"node"):
                resource_list.append( resource )
            return resource_list
        
    
    #todo verifier le super() 
    def __eq__(self, set ):

        if not super(ResourceSet, self).__eq__(set) or len(self.resources)!=len(set.resources) :
            return False

        for i in range(0,len(self.resources)-1) :
            if self.resources[i] != set.resources[i] :
                return False
        return True

    def __ne__(self, set ):
        return not (self==set)

    #Equality between to resoruce sets.
    def eql( self, set ) :
        if not super(ResourceSet, self).__eq__(set) or len(self.resources)!=len(set.resources) :
            return False

        for i in range(1,len(self.resources)-1) :
            if not self.resources[i].eql(set.resources[i]) :
                return False

        return True

    # Returns a ResourceSet with unique elements.
    # self.return [ResourceSet]     with unique elements
    def uniq(self):
        # set = copy.deepcopy(self)
        set = self.copy()
        return set.uniq_aux()
    

    def uniq_aux(self):
        i = 0
        # while i < len(self.resources) -1 :
        for i in range(len(self.resources) -1):
            pos = []
            for j in range(i+1,len(self.resources)):
                if self.resources[i].eql(self.resources[j]) :
                    pos.append(j)
                      
            for p in reversed(pos):
                del (self.resources[p])
            
            # i += 1 

        for resource in self.resources :
            if isinstance(resource, ResourceSet):
                resource.uniq_aux()
 
        return self
        

    # Generates and return the path of the file which contains the list of the type of resource
    #specify by the argument type.

    # def resource_file( type=None, update=False ) :
    #     if (( not self.resource_files[type] ) or update) :

    #             self.resource_files[type] = Tempfile("#{type}")
    #             resource_set = self.flatten(type)
    #             resource_set.each { |resource|
    #                     self.resource_files[type].puts( resource.properties[:name] )
    #             }( not self.resource_files(type) ) or update
    #             self.resource_files[type].close
        
    #     return self.resource_files[type].path
        

    #Generates and return the path of the file which contains the list  of the nodes' hostnames. Sometimes it is handy to have it.
    #eg. Use it with mpi.    
    #def node_file( update=False ):
    #    resource_file( "node", update )
        




    #alias nodefile node_file

    #propre a ruby
    
    #Generates a directory.xml file for using as a resources 
    #For Gush.
    # def make_gush_file( update = false):
    #     gush_file = File("directory.xml","w+")
    #     gush_file.puts("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    #     gush_file.puts("<gush>")
    #     resource_set = self.flatten(:node)
    #     resource_set.each{ |resource|
    #         gush_file.puts( "<resource_manager type=\"ssh\">")
    #         gush_file.puts("<node hostname=\"#{resource.properties[:name]}:15400\" user=\"lig_expe\" group=\"local\" />" )

    #         gush_file.puts("</resource_manager>")
    #     }
    #     gush_file.puts("</gush>")
    #     gush_file.close
    #     return gush_file.path
    

    #Creates the taktuk command to execute on the ResourceSet
    #It takes into account if the resources are grouped under
    #different gatways in order to perform this execution more
    #efficiently.
    def make_taktuk_command(self,cmd):
            str_cmd = ""
            #pd : separation resource set/noeuds
            if self.gw != "localhost" :
                sets =False
                sets_cmd = ""
                for resource in self.resources:
                   if isinstance(resource,ResourceSet) :
                       sets = True
                       
                   sets_cmd += resource.make_taktuk_command(cmd)
                if sets :
                    str_cmd += " -m "+ self.gw() +"-[ " + sets_cmd + " -]" 
                nodes = False
                nodes_cmd = ""
                
                for resource in self.resources:
                    if resource.type == "node" :
                        nodes = True
                        nodes_cmd += resource.make_taktuk_command(cmd)
                if nodes :
                    str_cmd += " -l "+  self.gw_ssh_user() +" -m "+ self.gw()+" -[ -l "+self.ssh_user()+" " + nodes_cmd + " downcast exec [ "+cmd+" ] -]" 
            else :
                nodes = False
                nodes_cmd = ""
                first = ""
                for resource in self.resources :
                    if resource.type == "node" :
                        if not nodes :   
                            first = resource.name 
                        nodes = True
                        nodes_cmd += resource.make_taktuk_command(cmd)
                
                print (" results of the command "+nodes_cmd )
                if nodes :
                    str_cmd += " -l "+ self.gw_ssh_user()+" -m "+ first +" -[ " + nodes_cmd + " downcast exec [ "+cmd+" ] -]" 
                    sets = False
                    sets_cmd = ""

                    for resource in self.resources :
                        if isinstance(resource,ResourceSet) :
                            sets = True
                            sets_cmd += resource.make_taktuk_command(cmd)
                    if sets :
                            if nodes : 
                                    str_cmd += " -m "+first + " -[ " + sets_cmd + " -]"
                            else:
                                    str_cmd += sets_cmd
                            
                    
            
            return str_cmd
        

#TODO :  2 pb :lit pas le premier resource_set si type = resource set 
#TODO :  pas de raise stopiteration dans getitem

class ResourceSetIterator:
        #current : element courant 
        #iterator : resource set pour parcourir les resource_set 
        #resource_set: la resource initale 
        #type : le type de la resource initiale
        #
        #
        #attr_accessor :current, :iterator, :resource_set, :type
        def __init__(self, resource_set, type=None):
                self.resource_set = resource_set
                self.iterator = None
                self.type = type
                self.current = 0
                self.debut = True 
                for i in range(len(resource_set.resources)) :
                    # print 'resource ' + str(i) + " est du type = "+ self.resource_set.resources[i].type
                    # print 'type demande est = ' + self.type
                    if self.type == self.resource_set.resources[i].type :
                        self.current = i
                        # print "courrent dans init = " +str(self.current) 
                        return 
                    elif isinstance(self.resource_set.resources[i],ResourceSet) :
                        self.iterator = ResourceSetIterator(self.resource_set.resources[i], self.type)
                        if self.iterator.resource :
                            self.current = i
                            if i!= 0 :
                                self.debut = False
                            return
                        else :
                            self.iterator = None
                                
                    elif not self.type :
                        self.current = i
                        if i!= 0 :
                            self.debut = False
                        return
                # print "dans la fin de init"
                self.current = len(self.resource_set.resources)
        
        def resource(self):
                if( self.current > len( self.resource_set.resources) ):
                    return None 
                if self.iterator :
                    res = self.iterator.resource()

                else :
                    res = self.resource_set.resources[self.current]
                
                return res
        

        def next(self):
            res = None
            if not self.iterator and not self.debut  :
                self.current += 1
            # print 'len = ' +  str(len(self.resource_set.resources)) + ' current =' + str(self.current)
            while not res and self.current < len(self.resource_set.resources) : 
                    # print "ici"
                    if self.iterator :
                            try :
                                res =self.iterator.next()
                            except StopIteration :
                                self.iterator = None
                                self.current += 1
                            #res = self.iterator.resource()
                            self.debut = False
                            
                    elif self.type == self.resource_set.resources[self.current].type :
                            res = self.resource_set.resources[self.current]
                            if self.type == "resource_set" :
                                self.iterator = ResourceSetIterator(self.resource_set.resources[self.current], self.type)


                            self.debut = False
                    elif isinstance(self.resource_set.resources[self.current],ResourceSet) :
                            self.iterator = ResourceSetIterator(self.resource_set.resources[self.current], self.type)
                            #res = self.iterator.resource()
                            try :
                                res =self.iterator.next()
                            except StopIteration :
                                self.iterator = None
                                self.current += 1
                                
                            self.debut = False
                    elif not self.type :
                            res = self.resource_set.resources[self.current]
                            self.debut= False
                    else:
                            self.current += 1
                    
            if not res:
                self.current = 0
                raise StopIteration
                return None 
            # if self.iterator :
            #     res = self.iterator.resource()

            # else :
            #     res = self.resource_set.resources[self.current]
            
            return res
                    
        def __iter__(self):
            return self




#function for xml parsing
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
    
    res = Resource(type,d_prop,name)

    return res 

#Rs_fomr_xml :
#
#
#@param : tree is the node of the resource_set
#@return : resource_set
def RS_from_xml(tree):
    resource_set = ResourceSet()
    
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

def parser_xml(path):
    tree = ET.parse(path) #'xml/rs1.xml'
    root = tree.getroot()
    return (RS_from_xml(root))

#### function to create xml from a resource_set 
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
        if isinstance(res,ResourceSet):
            resources.append(Rs_toxml(res))
            
        elif isinstance(res,Resource):
            resources.append(R_toxml(res))
    
    top.extend(resources)    
    
    n_t = ET.SubElement(top,"type")
    n_t.text = rs.type
    
    return top

def xml_writer(r):
    return prettify(Rs_toxml(r))
