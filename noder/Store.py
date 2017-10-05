
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
   @staticmethod
   def store(name,obj):
      key =  sys.argv[len(sys.argv)-1] #get the last arguement it will be the key
      data = read_object(key)
      data[name] = obj
      save_object(data,key)

   @staticmethod
   def retrive(name):
      key =  sys.argv[len(sys.argv)-1] #get the last arguement it will be the key
      data = read_object(key)
      if name in data:
         return data[name]
      else:
         #raise KeyError
         return None 

   @staticmethod
   def clear(filename): 
      if os.path.exists(filename) :
         os.remove(filename)
      

      
