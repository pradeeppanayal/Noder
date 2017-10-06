import sys


_author_ ="Pradeep CH"
_date_ ="5-Oct-2017"
_version_ ="1.0.0"


sys.path.append('.')

from noder import Store

dataStore = Store()
dataStore.store("data",34)

print "hai","script 1" 
