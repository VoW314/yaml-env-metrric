#Author: Shreyas Bera

from yaml.loader import SafeLoader
import yaml
import numpy as np


from rich.console import Console
from rich import inspect


console = Console()

#sources:
#https://github.com/Jjschwartz/NetworkAttackSimulator/blob/master/nasim/scenarios/benchmark/medium-multi-site.yaml
#https://networkattacksimulator.readthedocs.io/en/latest/tutorials/creating_scenarios.html
#https://networkattacksimulator.readthedocs.io/en/latest/tutorials/scenarios.html
"""
Validates the .yaml files before they are ran through NASIM.
Also tells the issue with mistakes within the file so that the 
user can fix them.

"""
class validate:
    # ~ Constructor --------------------------------
    def __init__(self, filename): 
        self.filename = filename
        
        with open(filename, 'r') as f:
            self.data = (yaml.load(f, Loader=SafeLoader))
        
        #gets data the enviroment file
        self.topology = self.data['topology']
        self.col = len(self.topology)
        self.row = len(self.topology[0])
    
    # ~ Public Methods --------------------------------
    def validation(self):
        """_summary_: checks the validity of the yaml files.
        This is a public method used in unpack.py

        Returns:
            _bool_: isValid
        """
        console.print(f"{self.filename.upper()}:", style = "bold underline")
        isValid = True
        
    
        if (not self.internet_connection()):
            isValid = False
            
        if (not self.__is_bidrectional()):
            isValid = False
        
        if (not self.__full_env()):
            isValid = False
        
        if (not self.__type_check()):
            isValid = False        
            
                 
        #if validation failed 
        if (isValid == False):
            console.print()
            console.print(f"X {self.filename} INVALID", style = "red")
            console.print()
            console.print(self.data)
           
        else:
            console.print(f"✓ {self.filename} VALID", style = "green")
        
        
        #return true if validation succeeded. false if not.
        console.print()
        return isValid
    
        
    def return_data(self):
        """
        returns:
            dictionary: many dictionaries containg the 
            components of the yaml file.
        """
        #subnets, sensitive hosts, os, services, processes, exploits, priv escalations, service cost, os cost, subnet cost, process cost, host configs, firewall
        return self.sb, self.sh, self.os, self.s, self.p, self.e, self.pe, self.ssc, self.osc, self.sbc, self.psc, self.hc, self.fw
            

    
    
    # ~ Private Methods --------------------------------
    
    def internet_connection(self):
        """_summary_
        
        1st check: 
        A 1 in the first row and column indicate that
        the network is connected to the internet. If the
        network is not connected to the internet, then an agent
        that comes from the internet will be unable to access the network.
        
        
        Returns:
            bool: True means it passes validation.
        """
        
        
        if (self.topology[0][0] == 1):
            
            return True
        else:
            console.print(f"> Is not connected to the internet. Make sure {0,0} is 1", style = "yellow")
            console.print()
            return False
        
    def __is_bidrectional(self):
        """
        _summary_
        Bidrectionality means the matrix is symmetrical.
        The method returns True if the matrix is bidirectional.
        
        Returns:
            bool: True if bidirectional. False if not. 
        """
        
        for i in range(self.col):
            for j in range(self.row):
                if(self.topology[i][j] != self.topology[j][i]):
                    console.print(f"> Unparallel matrix found at {self.topology[i][j]}", style="yellow")
                    console.print()
                    return False
                
        
        return True
        
    
    def __full_env(self):
        """_summary_
        Checks that all components ot the document topology exist
        """
        
        #sensitive hosts are dictionaries
        try:
            self.sb = self.data['subnets']
            self.sh = self.data['sensitive_hosts']
            self.os = self.data['os']
            self.s = self.data['services']
            self.p = self.data['processes']
            self.e = self.data['exploits']
            self.pe = self.data['privilege_escalation']
            
            self.ssc = self.data['service_scan_cost']
            self.osc = self.data['os_scan_cost']
            self.sbc = self.data['subnet_scan_cost']
            self.psc = self.data['process_scan_cost']
            
            self.hc = self.data['host_configurations']
            self.fw = self.data['firewall']  
            #make asserts for arrays and dictionaries
            return True
            
        except:
            console.print("> Unable to find all keys, maps, and lists found. Please read documentation", style="yellow")
            console.print()
            return False
        
        
    """
    ----------------------------------------------------------------
    Below is the start of the "Deeper checks". These check the data types
    within the YAML file to make sure they are correct. 
    ----------------------------------------------------------------
    """
        
    #EEE
    def __type_check(self):
        """_summary_
        
        Checks that the configurations are all correct
        Within the dictionary making sure it contains
        processes, os, and services.
        """
        isValid = True
        
        if(not self.__host_check()):
            isValid = False

        if(not self.__yaml_lists_check()):
            isValid = False
            
        if(not self.__costs()):
            isValid = False

        if(not self.__firewall_check()):
            isValid = False
            
        if(not self.__exploit_check()):
            isValid = False
        
        if(not self.__priv_check()):
            isValid = False
        

        return isValid
      
      
    def __yaml_lists_check(self):
        """_summary_
            Checks the subnets, topology, os, services, and processes

        Returns:
            _boolean_: Returns True subnets and topology are both arrays
        """
        isValid = True
        
        if(not isinstance(self.sb, list)):
            console.print(f"> Invalid subnets value type. Must be list, not {type(self.sb)}.", style = "yellow")
            isValid = False
            
        if (not isinstance(self.topology, list)):
            console.print(f"> Invalid topology value type. Must be list, not {type(self.toplogy)}.", style = "yellow")
            isValid = False 
            
        if(not isinstance(self.s, list)):
            console.print(f"> Invalid services value type. Must be list, not {type(self.s)}.", style = "yellow")
            console.print(f"> Invalid services type. Must be list, not {type(self.s)}.", style = "yellow")
            isValid = False
            
        if(not isinstance(self.p, list)):
            console.print(f"> Invalid processes value type. Must be list, not{type(self.p)}.", style = "yellow")
            isValid = False
        
        if (not isinstance(self.os, list)):
            console.print(f"> Invalid os value type. Must be list, not {type(self.os)}.", style = "yellow")
            console.print(f"> Invalid OS type. Must be list, not {type(self.os)}.", style = "yellow")
            isValid = False
            
        #makes a break in output to help make debugging easier   
        if (isValid == False):
            console.print()
            
        return isValid
    
    def __costs(self):
        #self.ssc, self.osc, self.sbc, self.psc,
        isValid = True
        
        if(not isinstance(self.ssc, int)):
            console.print(f"> Invalid service scan value type. Must be integer, not{type(self.ssc)}.", style = "yellow")
            isValid = False
        
        if(not isinstance(self.osc, int)):
            console.print(f"> Invalid OS scan type. Must be integer, not {type(self.osc)}.", style = "yellow")
            isValid = False
            
        if(not isinstance(self.sbc, int)):
            console.print(f"> Invalid subnet scan type. Must be integer, not{type(self.sbc)}.", style = "yellow")
            isValid = False
            
        if(not isinstance(self.psc, int)):
            console.print(f"> Invalid processes scan type. Must be integer, not{type(self.psc)}.", style = "yellow")
            isValid = False
            
            
        if (isValid == False):
            console.print()
        return isValid


    
    def __firewall_check(self):
        """_summary_: checks the validity of 

        Returns:
            _bool_: isValid
        """
        isValid = True
        for coord, config in self.fw.items():
            if(not isinstance(config, list)):
                console.print(f"> Invalid type at {coord}. Must be list, not{type(config)}.", style = "yellow")
                isValid = False
                
        if(isValid == False):
            console.print()
        return isValid
    
    def __exploit_check(self):
        """_summary_: checks the validity of exploits

        Returns:
            isValid: Boolean
        """
        isValid = True
        
        for coord, config in self.e.items():
            if (not all(key in config for key in ['service', 'os', 'prob', 'cost', 'access'])):
                    console.print(f"> Missing keys at {coord} in host configuration. Must include ['os', 'services', 'prob', 'cost', 'access']", style = "yellow")
                    isValid = False 
    
        if (isValid == False):
            console.print()
        return isValid
    
    def __priv_check(self):
        """_summary_: checks the validity of privilege escalations

        Returns:
            isValid: Boolean
        """
        isValid = True
        process_list = self.data['processes']
        
        priv_dict = self.data['privilege_escalation']
        
        os_list = ['linux']
        

        for key, value in priv_dict.items():
    
            #check that the process has already been defined
            if value['process'] not in process_list:
                console.print(f"> Invalid process found in 'privilige_escalation'. {value['process']} is undefined in 'processes at {key}' ", style="yellow")
                isValid = False
            
            #WIP. For some reason self.data['os'] returns 1 
            #if value['os'] not in os_list:
                #console.print(f"> Invalid os. This check is a WIP so isValid remains True", style = "yellow")
                #isValid = False
                
            #make sure that probability not > 1
            if (value['prob'] > 1.0 or value['prob'] < 0.0):
                console.print(f"> Invalid probability. Probability must be between 0 and 1, not {value['prob']} at {key}", style = "yellow")
                isValid = False
            
            #make sure that cost is an integer
            if (not isinstance(value['cost'], int)):
                console.print(f"> Invalid cost. Cost must be an integer at {key}")
                isValid = False
            
            #make sure access exists
            #WIP
                
            
                

        return isValid
    
    #RRR
    def __host_check(self):
        
        """_summary_
            Checks if the host configurations contains: 'os', 
            'services', and 'processes'. Then checks the values of each
            key to make sure they are the correct type

        Returns:
            _boolean_: Returns True if the host_configurations 
            are valid. False if there is an issue
        """
        isValid = True
        for coord, config in self.hc.items():
            

            try: 
                if (not all(key in config for key in ['os', 'services', 'processes'])):
                    console.print(f"> Missing keys in host configuration at {coord}. Must include ['os', 'services', 'processes']", style = "yellow")
                    console.print(f"> Missing keys at {coord} in host configuration. Must include ['os', 'services', 'processes']", style = "yellow")
                    isValid = False
            except:
                pass
            
            try:    
                if (not isinstance(config['os'], str)):
                    console.print(f"> Invalid os value type at {coord}. Must be a String, not {type(config['os'])}.", style = "yellow")
                    console.print(f"> Invalid OS value type at {coord} in host configuration. Must be a String, not {type(config['os'])}.", style = "yellow")
                    isValid = False
            except:
                pass
            
            try:    
                if (not isinstance(config['services'], list)):
                    console.print(f"> Invalid services value type at {coord}. Must be a list, not {type(config['services'])}.", style = "yellow")
                    console.print(f"> Invalid services value type at {coord} in host configuration. Must be a list, not {type(config['services'])}.", style = "yellow")
                    isValid = False
            except:
                pass
            
            try:
                if (not isinstance(config['processes'], list)):
                    console.print(f"> Invalid processes value type at {coord}. Must be a list, not {type(config['processes'])}.", style = "yellow")
                    console.print(f"> Invalid processes value type at {coord} in host configuration. Must be a list, not {type(config['processes'])}.", style = "yellow")
                    isValid = False
            except:
                pass
         
        #makes a break in output to help make debugging easier   
        if (isValid == False):
            console.print()
        return isValid
    
