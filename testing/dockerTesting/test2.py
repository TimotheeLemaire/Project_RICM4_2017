from execo import *
from subprocess import call
import subprocess

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

#targets = list(reversed(hosts))
remote = Remote("echo \"Hello world\"", hosts)
remote.run()

for s in remote.processes:
	print "%s\nstdout:\n%s\nstderr:\n%s" % (s, s.stdout, s.stderr)

#servers = Remote("nc -l -p 6543 > /dev/null", hosts)
#clients = Remote("dd if=/dev/zero bs=50000 count=125 | nc -q 0 {{targets}} 6543", hosts)
#with servers.start():
#	sleep(1)
#	clients.run()
#	servers.wait()

#print Report([ servers, clients ]).to_string()
#for s in servers.processes + clients.processes:
#	print "%s\nstdout:\n%s\nstderr:\n%s" % (s, s.stdout, s.stderr)






