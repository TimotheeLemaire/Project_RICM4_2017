from execo import *
from subprocess import call
import subprocess
import sys
sys.path.insert(0, '../../dev/')
import resourceSet

#create docker image.

call(["docker","build","-t","eg_sshd","."])
hosts = [None] * 10
for i in range (0, 10):
	name="test_ssdh"+str(i)
	#delete the previous container in case it exist
	call(["docker","rm","-f",name])
	#create docker container
	call(["docker","run","-d","-P","--name",name,"eg_sshd"])
	#get the port correspondoing to port 22 of the container
	p=subprocess.check_output(["docker","port",name,"22"])
	#build up hosts list
	hosts[i] = (Host(address='127.0.0.1',user='root',port=int(p[8:-1])))
	print hosts[i]


rsTest = resourceSet.ResourceSet("rsTest")
rs2 = resourceSet.ResourceSet("rs2")

rsTest.append(resourceSet.Resource(name='host0',host=hosts[0]))
rsTest.append(resourceSet.Resource(name='host1',host=hosts[1]))
rsTest.append(resourceSet.Resource(name='host2',host=hosts[2]))
rsTest.append(resourceSet.Resource(name='host3',host=hosts[3]))
rs2.append(resourceSet.Resource(name='host4',prop={'id':'42'},host=hosts[4]))
for i in range(5,9) :
	rs2.append(resourceSet.Resource(name='host'+str(i),host=hosts[i]))
rsTest.append(rs2)
rsTest.append(resourceSet.Resource(name='host9',prop={'id':'42'},host=hosts[9]))
# rsTest.append(resourceSet.Resource('node',name='nodeTest'))

raw_input()

print("Size of rsTest : ")
print(len(rsTest))

raw_input()

print("Size of rsTest flattened")
print(len(rsTest.flatten()))

raw_input()

print("nodes with id:42 in rsTest")
for r in rsTest.flatten().select(props={'id':'42'}) :
	print(r)

raw_input()

print("nodes from the inner resourceSet")
for r in rsTest.select(block=(lambda x : x.type=="resource_set")) :
	print(r)

raw_input()

xmlstring = resourceSet.xml_writer(rsTest)

print(xmlstring)

xmlfile = open('rs.xml', 'w')
xmlfile.write(xmlstring)
xmlfile.close()

raw_input()

newrs = resourceSet.parser_xml('rs.xml')

print("nouveau resourceSet = ancien resourceSet ?")

print(newrs.eql(rsTest))

raw_input()

newhosts = newrs.hosts()
print(hosts)

raw_input()

remote = Remote("echo \"Hello world\"", newhosts)
remote.run()

for s in remote.processes:
	print "%s\nstdout:\n%s\nstderr:\n%s" % (s, s.stdout, s.stderr)

