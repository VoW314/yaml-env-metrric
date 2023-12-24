from yaml.loader import SafeLoader
import pandas as pd 
import yaml
import numpy as np

from rich.console import Console
from rich.table import Table

class grade:
    def __init__(self, filename):
        self.filename = filename
        
        with open(filename, 'r') as f:
            self.data = (yaml.load(f, Loader=SafeLoader))
        
        #gets data the enviroment file
        self.topology = self.data['topology']
        self.hosts = self.data['host_configurations']
        self.sens=self.data['sensitive_hosts']
        self.fire=self.data['firewall']
        
        #row and column size variables
        self.row = len(self.topology)
        self.col = len(self.topology[0])
        
        #grading varaibles
        self.area = 0
        self.score = 0
        self.edges = 0 
    
    def unpack_hosts(self):
        """
        This function mainly just converts types 
        into different types that can be used later
        """
        
        array = np.zeros((self.row, self.col))
        
        #console
        table = Table(title="Host Table")
        table.add_column("Coordinates")
        table.add_column("OS")
        table.add_column("Services")
        table.add_column("Processes")
        
        console = Console()
        
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
                else:
                    processes =', '.join(value)
                    
      
            table.add_row(key, os, services, processes)
            
            key = key.replace(" ", "") #in the case that there is no " " in the yaml
            x = int(key[1])
            y = int(key[3])
            array[y,x] = 1
            

        
    
        #prints table to console for user view
        console.print(table)
        #return
        return array
