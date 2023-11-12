'''
This class does a deep first search made to be used on the yaml files
The code will do a deep first search algorithm. 


2 versions will be implemented:
1) This implementation will code works with just the blank topology. This is 
a basic version until the complete implementation and creation of the hardness class

2) This implementation will code works with the different values
and firewalls associated. This one is more complex and will be implemented 
when the hardness class is completed. 

Author Shreyas B
'''

#imports
import pandas as pd
import numpy as np
import yaml
from hardness_class.py import * 

#code actual
class dfs:
    def __init__(self, filename):
        self.filename = filename
        
        with open(filename, 'r') as f:
            self.data = (yaml.load(f, Loader=SafeLoader))
        
        self.topology = self.data['topology']
        self.end(0,0) #ending coordinates

    
    def get_ends(self):
        #assigns user input values into the ending coordinates
        #always will start at 0,0 so we don't need user input starts
        x = int(insert("x-coordinate ending: "))
        y = int(insert("y-coordinate ending: "))
        return self.end(x,y)
    
    def dfs_start(self, matrix, start, end):
        self.rows, self.cols = len(matrix), len(matrix[0])
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.path = []
        
    #actual do things
    def do_dfs(self):
        pass
    
        