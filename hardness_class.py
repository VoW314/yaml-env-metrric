from yaml.loader import SafeLoader
import pandas as pd 
import yaml




#scores
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
    
    def cell_count(self, matrix, row, col):
        rows, cols = len(matrix), len(matrix[0])
        ones = 0
        
        # kernel
        #gets the cell above, below, left, and right of current cell
        kernel = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in kernel:
            r, c = row + dr, col + dc
            #finds the number of ones within the kernel
            if 0 <= r < rows and 0 <= c < cols:
                if matrix[r][c] == 1:
                    ones += 1
        
        return ones
    
    def one_count(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        counts_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for row in range(rows):
            for col in range(cols):
                ones = self.cell_count(matrix, row, col)
                counts_matrix[row][col] = ones
        
        return counts_matrix
    
    def score(self):
        top_matrix = self.one_count(self.topology)
        
        for x in self.sens:
            coordinate_string = x
            coordinate_list = [int(x) for x in coordinate_string.strip('()').split(',')]
            row, col = coordinate_list
            #multiply the matrix by the sensitivity score
            top_matrix[row][col] = top_matrix[row][col] * SENS_SCORE
        
        for x in self.fire:
            coordinate_string = x
            coordinate_list = [int(x) for x in coordinate_string.strip('()').split(',')]
            row, col = coordinate_list
            #multiply the matrix by the sensitivity score
            top_matrix[row][col] = top_matrix[row][col] * FIRE_SCORE
        
        return top_matrix
    
        