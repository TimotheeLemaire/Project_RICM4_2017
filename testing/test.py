import yaml
import ressourceSet

#import os
#os.system("python ../dev/ressourceSet.py")

def test_yaml():
	with open('resource_set2.yaml', 'r') as f:
		res = yaml.load(f)

def test_resource():

	with open('resource_set2.yaml', 'r') as f:
		res = yaml.load(f)
		r = ressourceSet.Resource(res["type"],res["properties"],res["properties"]["name"])
	#print(res)
	print(str(r))

test_resource()