from execo import *
hosts = [ Host("192.168.99.100", user='docker'), Host("192.168.99.101", user='docker')]
targets = list(reversed(hosts))
servers = Remote("nc -l -p 6543 > /dev/null", hosts,{'scp_options': ('-o', 'PasswordAuthentication=no',)})
clients = Remote("dd if=/dev/zero bs=50000 count=125 | nc -q 0 {{targets}} 6543", hosts)
with servers.start():
  sleep(1)
  clients.run()
  servers.wait()
print Report([ servers, clients ]).to_string()
for s in servers.processes + clients.processes:
  print "%s\nstdout:\n%s\nstderr:\n%s" % (s, s.stdout, s.stderr)
