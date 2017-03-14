from execo import *
process = Process("ls ")
process.run()
print "process:\n%s" + str(process)
print "process stdout:\n" + process.stdout
print "process stderr:\n" + process.stderr
