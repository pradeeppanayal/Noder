
import os
import json

import shlex
import subprocess
import uuid
from noder import Store

_author_ ="Pradeep CH"
_date_ ="4-Oct-2017"
_version_ ="1.0.0"


class ExecutionException(Exception):
   pass
 
class Script(object):
   def __init__(self):
      self.name = ""
      self.preScripts= []
      self.completedPreScripts =0
      self.status = "Pending"
      self.error = ""
      self.output = ""
      self.order = -1

   def load(self,data):
      assert "name" in  data.keys(),"Invalid input param should have \"name\"."
      assert "preScripts" in  data.keys(),"Invalid input param should have \"preScripts\"."

      self.name = data['name']
      self.preScripts= data['preScripts']

   def __str__(self):
      return "[name :" + str(self.name) + ", Prescript count :"+ str(len(self.preScripts)) + ", Order : "+ str(self.order) +", Status :" + self.status +", output :"+self.output+", Error :"+str(self.error)+ "]";

class ExecutionItem(object):
   def __init__(self,script,order=0):
      self.script = script
      self.order = order
   
class FlowManager(object):
   def __init__(self,flowFilePath,sourceFilePath):
      self.flowFilePath = flowFilePath
      self.sourceFilePath = sourceFilePath
      self.scripts = {}
      self.maxOrder = 0

   def _validateInputs(self):
      assert os.path.exists(self.flowFilePath),"The file %s cannot be found " %self.flowFilePath
      assert os.path.exists(self.sourceFilePath),"The path %s cannot be found " %self.sourceFilePath

   def _loadScripts(self):
      data = ""
      with open(self.flowFilePath,"r") as f:
         data = f.read()
      _scriptsInJsonFormat = json.loads(data)
      assert "scripts" in _scriptsInJsonFormat.keys(),"Invalid input param should have \"scripts\"."

      for item in  _scriptsInJsonFormat['scripts']:
         script = Script()
         script.load(item)
         self.scripts[script.name] = script

   def _getOrder(self,currentItemName,visitedNodes = []):     
      item = self.scripts[currentItemName]

      #already set
      if item.order != -1:
         return item.order

      #Validate for loop
      if  currentItemName in visitedNodes:
         raise ExecutionException,"Loop detected at " + currentItemName

      #Add the visited node
      visitedNodes.append(currentItemName)

      #No pre scripts means order will be 1
      if len(item.preScripts) == 0:
         return 1

      subOrders = []
      for preScriptName in item.preScripts:
          prescript = self.scripts[preScriptName] 
          prescriptOrder = self._getOrder(preScriptName,visitedNodes)
          prescript.order= prescriptOrder
          subOrders.append(prescriptOrder)

      return max(subOrders) + 1

   def _frameExecutionFlow(self):
      for key in  self.scripts.keys():
         item = self.scripts[key] 
         scriptOrder = self._getOrder(key)
         item.order = scriptOrder

   def _getScriptByOrder(self,currentOrder):
      return [i for i in self.scripts.values() if i.order==currentOrder]

   def _executeScript(self,script,key):      
       store = Store(key) 
       script.status ="Executing"
       fullPath = self.sourceFilePath +"/"+script.name+".py"
       interpreter  = "python"
       executionResponse = ''
       try:
          cmd = '%s %s %s' %(interpreter,fullPath,key) 
          p =  subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False)
          executionResponse, err = p.communicate()
          if err:    
             script.status ="Failed" 
          else:
             script.status ="Success"    
          script.output = executionResponse
          script.error = err
          store.store(script.name,script)
       except Exception as e:  
          #TODO LOG
          script.error = e.message
          script.status ="Failed" 

   def _validatePreScripts(self,script):
       for item in script.preScripts:
          if self.scripts[item].status != "Success":
             return False
       return True

   def _executeScripts(self,orderedScripts,key):
       #TODO execute parallel
       for script in orderedScripts:
          if self._validatePreScripts(script):
             self. _executeScript(script,key)
          else:
             script.status = "Skipped"
             script.error = "Pre script(s) failed"

   def _executeByOrder(self):
      key = str(uuid.uuid4())
      store = Store(key)
      try:
         for i in range(1,self.maxOrder+1):
            orderedScripts= self._getScriptByOrder(i)
            self._executeScripts(orderedScripts,key)
      finally:
          store.clear()

   def _findMaxOrder(self):
      self.maxOrder = max([i.order for i in self.scripts.values() ])

   def execute(self):     
      self._validateInputs()
      self._loadScripts()
      self._frameExecutionFlow()
      self._findMaxOrder()
      self._executeByOrder() 

      for item in self.scripts.values():
         print item

if __name__ =="__main__":
    f = FlowManager("executionConfig.json","lab")
    f.execute()
   
