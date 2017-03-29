import yaml
import os

os.system("python ../dev/ressourceSet.py")

def test_yaml():
	with open('resource_set2.yaml', 'r') as f:
		res = yaml.load(f)

	print(res["properties"]["name"])

def test_resource():

	with open('resource_set2.yaml', 'r') as f:
		res = yaml.load(f)
		Resource(res["type"],res["properties"],res["properties"]["name"])
	#print(res)
	print(res.name())

test_resource()