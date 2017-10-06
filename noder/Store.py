
import sys
import pickle
import os

_author_ ="Pradeep CH"
_date_ ="5-Oct-2017"
_version_ ="1.0.0"

tempFolder = "/tmp/"

def save_object(obj, filename):
    with open(tempFolder + filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def read_object(filename):
    fullPath = tempFolder + filename
    if not os.path.exists(fullPath) :
       return {}

    with open(fullPath, 'rb') as f:
        return pickle.load(f)

class Store(object):
   def __init__(self,storename = None):
      self.storename = storename
      if storename == None:
         assert len(sys.argv) > 1,"Argument should contain unique store name"
         self.storename =  sys.argv[len(sys.argv)-1] #get the last arguement it will be the key  

   def store(self,name,obj):
      data = read_object(self.storename)
      data[name] = obj
      save_object(data,self.storename)

   def retrive(self,name):
      data = read_object(self.storename)
      if name in data:
         return data[name]
      else:
         #raise KeyError
         return None 

   def clear(self): 
      if os.path.exists(self.storename) :
         os.remove(self.storename)
      

      
