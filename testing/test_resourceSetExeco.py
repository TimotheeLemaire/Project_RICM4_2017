import sys
sys.path.insert(0, '../dev/')
import resourceSet
import execo

r=resourceSet.ResourceSet()
r.append(resourceSet.Resource('node',{'gateway':'127.0.0.1'}))

h = r.host()

print h
