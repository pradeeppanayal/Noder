import sys

sys.path.append('.')

from noder import Store

print "hai","script 3"
dataStore = Store()
print dataStore.retrive("data")
