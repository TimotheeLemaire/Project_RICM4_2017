import sys
sys.path.insert(0, '../dev/')
import resourceSet
import execo

r=resourceSet.ResourceSet()
r.append(resourceSet.Resource('node',{'gateway':'127.0.0.1','port':'1'}))
r.append(resourceSet.Resource('node',{'gateway':'127.0.0.1','port':'2'}))
r2=resourceSet.ResourceSet()
r2.append(r)
r2.append(resourceSet.Resource('node',{'gateway':'127.0.0.1','port':'3'}))

h = r2.hosts()[1]

r = resourceSet.Resource( host = h, prop={'name':'boustricoule'})

print r.properties