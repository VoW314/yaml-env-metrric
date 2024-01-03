from yaml.loader import SafeLoader
import yaml
import numpy as np



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
        print("Validating")
        if(self.has_internet_connection()):
            if (self.is_bidrectional()):
                if(self.full_env()):
                    return True
                raise AssertionError("Not All Components were found")
            raise AssertionError("The environment is not bidirectional")
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
            _type_: bool. True means it passes validation.
        """
        
        
        if (self.topology[0][0] == 1):
            return True
        else:
            return False
        
    def is_bidrectional(self):
        """
        _summary_
        
        A method that compares the topology to
        its transpose to find the if the 
        network is bidirectional. Using Linear Alg. we 
        know the transpose of the topology and the original
        will be the same if they topology is symmetrical. 
        
        Uses the numpy transpose for arrays
        
        Returns:
            _type_: bool. True means it passes validation.
        """
        
        #row = col or it won't work. Also NASIM won't work properly so this check is made. 
        if (self.row != self.col):
            return False
        
        transposed= np.transpose(self.topology) #transposes the topology        
        return np.allclose(self.topology, transposed, rtol=0, atol=0) #compares with tolerance of 0
    
        #if this doesn't work like intended implement something like below
        """
        for i in range(len(self.topology)):
            for j in range(len(self.topology):
                if(self.topology[i][j] != self.topology[j][i]):
                    return False
                
        return True
        """
    
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
        except:
            return False
        
    def return_data(self):
        """
        returns all the components
        """
        #subnets, sensitive hosts, os, services, processes, exploits, priv escalations, service cost, os cost, subnet cost, process cost, host configs, firewall
        return self.sb, self.sh, self.os, self.s, self.p, self.e, self.pe, self.ssc, self.osc, self.sbc, self.psc, self.hc, self.fw
    
        
        
    
    
        
        
              
