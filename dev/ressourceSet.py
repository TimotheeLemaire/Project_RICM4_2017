
#A Resource maps a computational resource to an object which keeps 
#Certains characteritics such as type, name, gateway.
class Resource():
	"""docstring for Resource"""
	self.Type #type of the resource
	self.properties #properties of the resources


    # Creates a new Resource Object.
    # @param [type] type of the source
    # @param [properties] object property
    # @param [String] String name
	# @return [resource] Resource Object
	def __init__(typ, prop=None , name = None):
		self.Type = types
		self.properties = dict() 

		if prop: #test si prop est vide 
			#----replaces the contents of @properties hash with
            #----contents of 'properties' hash
        	self.properties = prop  

		if name :
			self.properties["name"] = name 


	




