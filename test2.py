from execo import *
hosts = [ "192.168.99.101", "192.168.99.102", "192.168.99.103", "192.168.99.104" ]
targets = list(reversed(hosts))
servers = Remote("./123Soleil", hosts)
with servers.start():
  sleep(1)
  servers.run()
print Report([ servers, clients ]).to_string()
for s in servers.processes + clients.processes:
  print "%s\nstdout:\n%s\nstderr:\n%s" % (s, s.stdout, s.stderr)
