#Author: Shreyas Bera

from yaml.loader import SafeLoader
import pandas as pd 
import yaml
import numpy as np
from validation import *

from rich.console import Console
from rich.table import Table

console = Console()

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
        
    def exploitable_services(self):
        """
        Returns a list of 3 numbers with the counts of the processes
        [schtask, daclsvc, tomcat] multiplied by their respective probabilities
        
        Did not do a dictionary as this code already has too many dictionaries
        """
        config = self.host_configs
        escalation = self.priv_esc
   
        #[schtask, daclsvc, tomcat]
        process_count = [0,0,0]
        probs = [0,0,0]

        #get values of counts
        for coord, value in config.items():
            for word in value['processes']:
                if(word == "schtask"):
                    process_count[0] += 1
                elif(word == "daclsvc"):
                    process_count[1] += 1
                elif(word == "tomcat"):
                    process_count[2] += 1
         
        #get probs of each priv_esc           
        for key, value in escalation.items():
            if(key == "pe_schtask"):
                probs[0] = value['prob']
            elif(key == "pe_daclsvc"):
                probs[1] = value['prob']
            elif(key == "pe_tomcat"):
                probs[2] = value['prob']
                
         
        #numpy to do matrix multiplication       
        m1, m2 = np.array(process_count), np.array(probs)
    
        return np.multiply(m1, m2)
    
    
    def scan_costs(self):
        """
        Calculations based on scan_costs, priv_escalations, and exploit costs
        
        priv_escalation * access. 0.5 for user, 1 for root
        
        Return:
        >  scan_costs = [service_scan_cost, os_scan_cost, subnet_scan_cost, process_scan_cost]
        >  pe_costs   = [schtask, daclsvc, tomcat]
        >  exp_costs  = {'ssh': n , 'ftp': n, ...}
            
        """
        #scan cost
        scan_costs = [self.ssc, self.osc, self.sbc, self.psc]
        
        #pe_costs
        escalation = self.priv_esc
        pe_costs = [0,0,0]
        access = [0,0,0]
        
        for key, value in escalation.items():
            if(key == "pe_schtask"):
                pe_costs[0] = value['cost']
                access[0] = self.__access_factor(value['access'])
                
            elif(key == "pe_daclsvc"):
                pe_costs[1] = value['cost']
                access[1] = self.__access_factor(value['access'])
                
            elif(key == "pe_tomcat"):
                pe_costs[2] = value['cost']
                access[2] = self.__access_factor(value['access'])
                
        m1 = np.array(pe_costs)
        m2 = np.array(access)
        
        pe_costs = np.multiply(m1, m2)
        
        #exp_costs
        exp_costs = {}

        """
        Write in dictionary as 'service name' : 'acces cost calculation'
        
        For example medium yields:
            {'ssh': 0.5, 'ftp': 1, 'http': 0.5, 'samba': 1, 'smtp': 0.5}
            
        """
        for key, value in self.exploits.items():
            exp_costs[value['service']] = self.__access_factor(value['access'])

        return scan_costs, pe_costs, exp_costs 
    
    def segmentation(self):
        pass
                

    def __access_factor(self, value):
        """
        Private method in the case that user and root
        are not the only two values for a specific privilege_escalation
        or exploit
        """
        #user
        if(value == "user"):
            return 0.5
        else:
            #root
            return 1
            
        
    def subnet_calcualtions():
        number_of_subnets = len(self.subnets)
        
        #the first subnet is the DMZ of the network
        pass
        
            
    
    