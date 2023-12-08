'''
This class grades the yaml files for dificulty. It does this by 
getting the attributes of the yaml file and preforming basic calculations

Author: Shreyas B.
'''



#imports
from yaml.loader import SafeLoader
import pandas as pd 
import yaml




#scores
#arbitrary values I gave
SENS_SCORE = 0.5
FIRE_SCORE = 1.5

class hardness:
    def __init__(self, filename):
        self.filename = filename
        
        with open(filename, 'r') as f:
            self.data = (yaml.load(f, Loader=SafeLoader))
        
        self.topology = self.data['topology']
        
        self.sens=self.data['sensitive_hosts']
        self.fire=self.data['firewall']
        
        self.area = 0
        self.score = 0
        self.edges = 0 
        self.br="\n"
        
    def original_top(self):
        return self.topology

    
    def score(self):
        top_matrix = self.one_count(self.topology)
        
        #sensitive hosts
        for x in self.sens:
            coordinate_string = x
            coordinate = [int(x) for x in coordinate_string.strip('()').split(',')]
            row, col = coordinate
            #multiply the matrix by the sensitivity score
            top_matrix[row][col] = top_matrix[row][col] * SENS_SCORE
        
        #firewalls
        for x in self.fire:
            coordinate_string = x
            coordinate = [int(x) for x in coordinate_string.strip('()').split(',')]
            row, col = coordinate
            #multiply the matrix by the sensitivity score
            top_matrix[row][col] = top_matrix[row][col] * FIRE_SCORE
        
   
        return top_matrix
    
    def average_grade(self):
        #gets the sum of all values in the matrix
        total = 0

        for row in self.score():
            for value in row:
                total += value
        
        #gets the average of all values in the matrix
        #average = total score / number of cells
        
        row = len(self.topology)
        col = len(self.topology[0])
        area = row * col
        average = total / area
        self.area = area
        
        #every host can be attacked again 
        #also every host can be linked to another host in the attacks
        edges = area * area
        self.edges = edges
        
        
        return average, area, edges
    
    def get_last_host(self):
        """
        This will get the last host in the environment.
        Returns coorindates of this host to be used by the 
        dfs class.
        """
        x_cord = 0
        y_cord = 0
        
        for i in range(len(self.topology)):
            for j in range(len(self.topology[0])):
                if self.topology[i][j] == 1:
                    last_host = (i,j)
        
        return last_host
    
    def return_matrix(self):
        return self.one_count(self.topology)
    
    
