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

class validate:
    def __init__(self, filename): 
        self.filename = filename
        
        with open(filename, 'r') as f:
            self.data = (yaml.load(f, Loader=SafeLoader))
        
        #gets data the enviroment file
        self.topology = self.data['topology']
        self.col = len(self.topology)
        self.row = len(self.topology[0])
    
    #DDD
    def validation(self):
        console.print(f"{self.filename.upper()}:", style = "bold underline")
        isValid = True
        
    
        if (not self.internet_connection()):
            isValid = False
            
        if (not self.is_bidrectional()):
            isValid = False
        
        if (not self.full_env()):
            isValid = False
        
        if (not self.type_check()):
            isValid = False        
            
                 
        #if validation failed 
        if (isValid == False):
            console.print(f"- {self.filename} INVALID", style = "red")
            console.print()
            console.print(self.data)
           
        else:
            console.print(f"- {self.filename} VALID", style = "green")
        
        
        #return true if validation succeeded. false if not.
        console.print()
        return isValid
    
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
            return False
        
    def is_bidrectional(self):
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
                    return False
                
        return True
        
    
    def full_env(self):
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
            return False
        
        
        
    #EEE
    def type_check(self):
        """_summary_
        
        Checks that the configurations are all correct
        Within the dictionary making sure it contains
        processes, os, and services.
        """
        isValid = True
        
        if(not self.host_check()):
            isValid = False
        
        if(not self.yaml_lists_check()):
            isValid = False
        
        
        
        
        return isValid
      
    def yaml_lists_check(self):
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
            isValid = False
            
        if(not isinstance(self.p, list)):
            console.print(f"> Invalid processes value type. Must be list, not{type(self.p)}.", style = "yellow")
            isValid = False
        
        if (not isinstance(self.os, list)):
            console.print(f"> Invalid os value type. Must be list, not {type(self.os)}.", style = "yellow")
            isValid = False
            
        return isValid
        
        
        
    def sensitive_host_check(self):
        pass
    
    
    
    
    #RRR
    def host_check(self):
        
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
                    isValid = False
            except:
                pass
            
            try:    
                if (not isinstance(config['os'], str)):
                    console.print(f"> Invalid os value type at {coord}. Must be a String, not {type(config['os'])}.", style = "yellow")
                    isValid = False
            except:
                pass
            
            try:    
                if (not isinstance(config['services'], list)):
                    console.print(f"> Invalid services value type at {coord}. Must be a list, not {type(config['services'])}.", style = "yellow")
                    isValid = False
            except:
                pass
            
            try:
                if (not isinstance(config['processes'], list)):
                    console.print(f"> Invalid processes value type at {coord}. Must be a list, not {type(config['processes'])}.", style = "yellow")
                    isValid = False
            except:
                pass
            
        
        return isValid
            
            
    def return_data(self):
        """
        returns:
            dictionary: many dictionaries containg the 
            components of the yaml file.
        """
        #subnets, sensitive hosts, os, services, processes, exploits, priv escalations, service cost, os cost, subnet cost, process cost, host configs, firewall
        return self.sb, self.sh, self.os, self.s, self.p, self.e, self.pe, self.ssc, self.osc, self.sbc, self.psc, self.hc, self.fw
    
        
        
    
    
        
        
              
