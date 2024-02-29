from yaml.loader import SafeLoader
import pandas as pd 
import yaml
import numpy as np
from validation import *

from rich.console import Console
from rich.table import Table

class grade:
    def __init__(self, filename):
        self.filename = filename
        
        with open(filename, 'r') as f:
            data = (yaml.load(f, Loader=SafeLoader))
        
        #gets data the enviroment file
        self.topology = data['topology']
        #row and column size variables
        self.col = len(self.topology)
        self.row = len(self.topology[0])
        
        #does a file validation on the yaml
        is_valid = validate(filename)        
        
        #check the validation
        if (is_valid.validation() == True):
            #very long unpacking of validation
            self.subnets, self.sens_hosts, self.os, self.services, self.processes, self.exploits, self.priv_esc, self.ssc, self.osc, self.sbc, self.psc, self.host_configs, self.fire = is_valid.return_data() 
            
            #grading varaibles
            self.area = self.row ^ 2
            
            self.score = 0
        else:
            raise TypeError("There is an issue in the yaml file. Validation returned False.")
        
        #no longer need the validation object
        del is_valid
        
    
   

        
    
    def host_table(self):
        """
        This function mainly just converts types 
        into different types that can be used later
        """
        
        #console
        table = Table(title="Host Table")
        table.add_column("(Subnet#, Host#)")
        table.add_column("OS")
        table.add_column("Services")
        table.add_column("Processes")
        
        console = Console()
        self.hosts = self.host_configs
        """
        Unpacks the host dictionary from the yaml file
        """
        for key, value in self.hosts.items():
            #string, dictionary
            for parts, value in value.items():
    
                if (parts == 'os'):
                    os = ''.join(value)
                elif (parts == 'services'):
                    services = ', '.join(value)
                elif (parts =="processes"):
                    processes =', '.join(value)
                else:
                    pass
                    
      
            table.add_row(key, os, services, processes)
            
        #prints table to console for user view
        console.print(table)
        
        """
        A tougher environment can best be defined by the one
        that the agent solves after a long time and get a lower score. 
        
        
        Now: 
        -----------
        Exploitable Services
        - Check the # of hosts w/ an exploit
        - Check the probability of the said exploid
        
        Costs of Scan
        - High cost of scans and actions will reduce the 
        final reward of the agent through the enivonrmnet
            > Issue caused by two similar files where one has
            higher costs and the other has lower costs would 
            make the grade better
        
        Segmentation (Basic)
        - Number of total subnets not including the DMZ and internet
        - Number of subnets w/ and w/o sensitive hosts
        - Distance form DMZ to the sensitive host via firewall and subnet
        connections
            > Tag the subnets with sensitive hosts and differentiate them
            from those without sensitive hosts
            
        Later: 
        -------------
        Segmentation (Advanced)
        - Difficulty to also crack the hosts themself
        - Firewall type and difficulty to pass check
        """
        
        
        
    def subnet_calcualtions():
        number_of_subnets = len(self.subnets)
        
        #the first subnet is the DMZ of the network
        pass
        
            
    
    