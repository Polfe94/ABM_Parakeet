import os
path = os.path.dirname(os.path.dirname(__file__)) + os.sep
folder = None
result_path = path + 'results/'
file_name = 'test' 

#Model
n_agents = 100 # 250
n_steps  = 0 #300000 # 800000
retrieve_positions = True

start_node = (0,22)
adulthood = 3 # age of becoming an adult

#Lattice size
width    = 22   
height   = 13  

#Parameters
'''
a
b
c
'''

#Number of different runs to average results
n_runs = 100
run_parallel = True

'''
POSSIBLE (DISTINCT) DISPERSAL STRATEGIES (?)
'''

