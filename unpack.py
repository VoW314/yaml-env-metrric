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
        
        if (self.validation() == True):
            self.hosts = self.data['host_configurations']
            self.sens=self.data['sensitive_hosts']
            self.fire=self.data['firewall']
            
            #row and column size variables
            self.row = len(self.topology)
            self.col = len(self.topology[0])
            
            #grading varaibles
            self.area = self.row * self.col
            
            self.score = 0
        
    def validation(self):
        """_summary_
        A 1 in the first row and column indicate that
        the network is connected to the internet. If the
        network is not connected to the internet, then an agent
        that comes from the internet will be unable to access the network.
        
        
        Returns:
            _type_: bool. True means it passes validation.
        """
        
        
        if (self.topology[0][0] == 1):
            return True
        else:
            return False
    
    
    """
    _Summary_
    
    Below code is the actual unpacking of the network data
        
    """
    
    def cell_count(self, row, col):
        ones = 0
        
        # kernel
        #gets the cell above, below, left, and right of current cell
        #think of it like a cross or plus sign 
        kernel = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in kernel:
            r, c = row + dr, col + dc
            #finds the number of ones within the kernel
            if 0 <= r < self.row and 0 <= c < self.col:
                if self.topology[r][c] == 1:
                    ones += 1
        
        return ones
    
    def one_count(self):
        counts_matrix = [[0 for _ in range(self.col)] for _ in range(self.row)]
        
        for row in range(self.row):
            for col in range(self.col):
                ones = self.cell_count(row, col)
                counts_matrix[row][col] = ones
        
        return counts_matrix

        
    
    def unpack_hosts(self):
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
    
    def top_tree(self):
        """
        Creates a tree diagram for the topology
        using the rich library
        """


        

        # firewalls are dictionary
        for key,value in self.fire.items():
            print(key,value)
        
        
        