# Noder
It is a frame work application for executing multiple python scripts with respect to a configurable execution flow. 
# How it works ??
 All the scripts are treated as a node in a directed graph.Only if all the prescripts are executed without error, then only a node/script will execute.
 Once a script executed and the status will be changed accordgly. If a prescript fails, then the script will be skipped.
# Features
* Configurable execution flow
* Detection of loops
* Shared store 
# Shared Store
* We can store and retrive values across the execution
    
#Sample configuration
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
   	},{
   		"name":"script4",
   		"preScripts":["script5","script6"]		
   	},{
   		"name":"script5",
   		"preScripts":["script6"]		
   	},{
   		"name":"script6",
   		"preScripts":["script4"]		
   	}
      ]
       
   }
   }
