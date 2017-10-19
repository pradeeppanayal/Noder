# Noder
It is a frame work application for executing multiple python scripts with respect to a configurable execution flow. 
# How it works ??
 * All the scripts are treated as a node in a directed graph.Only if all the prescripts are executed without error, then only a node/script will execute.
 * Once a script executed and the status will be changed accordgly. 
 * If a prescript fails, then the script will be skipped.
# Features
 * Configurable execution flow
 * Detection of loops
 * Shared store 
# Shared Store
 * We can store and retrive values across the execution
 * Store 
 
       from noder import Store
       dataStore = Store()
       dataStore.store("data",34) # Store value 34 with the ref name "data"
 * Retrive
        
       from noder import Store
       dataStore = Store()
       print dataStore.retrive("data")
 * User can store and retrive any python objects (Not limted to string and numbers)
 * State of a node/script will be auto saved to the store. You can get it back using the script name as ref name.
 * Store will be removed once all the node/script are executed.
 
# Sample configuration
       
    {   
      "scripts":[
   	   {
   		     "name":"script1",
   		     "preScripts":[]		
   	   },{
   		      "name":"script2",
   		      "preScripts":[]		
   	    },{
   		      "name":"script3",
   		     "preScripts":["script1","script2"]		
   	    } 
      ] 
    }
    
# Execution 
 * Sample code
 
       from noder import FlowManager
       f = FlowManager(executionFlow,scriptSource)
       f.execute()
       
  * executionFlow : Path to the json file which has the rules defined.   * scriptSource : Path of the directory in which all the script files are available.
