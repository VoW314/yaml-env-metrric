from yaml.loader import SafeLoader
import yaml
import numpy as np
from rich.console import Console
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
    
    def validation(self):
        if(self.has_internet_connection()):
            if (self.is_bidrectional()):
                if(self.full_env()):
                    console.print("- "+self.filename + " valid", style = "green")
                    return True
                
                else:
                    raise AssertionError("Not All Components were found")
            else:
                raise AssertionError("The environment is not bidirectional")
        else:
            raise ValueError("There is no internet connection")
        
        #default return false
        return False
    
    def has_internet_connection(self):
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
            return True
            
        except:
            return False
        
    def return_data(self):
        """
        returns:
            dictionary: many dictionaries containg the 
            components of the yaml file.
        """
        #subnets, sensitive hosts, os, services, processes, exploits, priv escalations, service cost, os cost, subnet cost, process cost, host configs, firewall
        return self.sb, self.sh, self.os, self.s, self.p, self.e, self.pe, self.ssc, self.osc, self.sbc, self.psc, self.hc, self.fw
    
        
        
    
    
        
        
              
