#
# Sample usage of Party
# Extracting artifact properties
# 
import os, sys
from party import *

artifact = Party()

# Example properties used assuming Bamboo CI
myProps = {
	"build.number": 189, # ${bamboo.buildNumber}
}

res = artifact.find_by_properties(myProps)
if res is None:
	print "No artifact found."
	sys.exit(1)

res = artifact.get_properties(artifact.uri)

for k in artifact.properties:
	for v in artifact.properties[k]:
                print "%s: %s" % (k, v)

for a in artifact.list:
	print a

print artifact.count
