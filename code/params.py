import os
import sys
import pandas as pd

path = os.path.dirname(os.path.dirname(__file__)) + os.sep
folder = None
result_path = path + 'results' + os.sep
file_name = 'test' 

#Model
n_agents = 100 # 250
n_steps  = 0 #300000 # 800000
retrieve_positions = True

# two options: center, random
start_node = 'center' # 'random'
adulthood = 3 # age of becoming an adult

#Lattice size (should have odd coordinates)
width    = 101  
height   = 101

if width % 2 != 0:
    width += 1

if height % 2 != 0:
    height += 1

kernel = 0 ## change to a distribution of dispersal !


# Parameters
''' LIFE TABLE '''
try:
    df = pd.read_csv(path + 'data' + os.sep + 'life_table.csv')
except:
    print('COULD NOT FIND LIFE TABLE. Exiting program...')
    sys.exit(1)


mu = 0.1 # mortality
rho = 0.5 # reproduction
gamma = 1 # growth 

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

