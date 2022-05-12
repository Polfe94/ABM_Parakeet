import os
import sys
import pandas as pd
import numpy as np

path = os.path.dirname(os.path.dirname(__file__)) + os.sep
result_path = path + 'results' + os.sep
file_name = 'test' 


""" MODEL PARAMETERS """
n_agents = 10
n_steps  = 200
starting_age = 2

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


# function with probability as input, jump distance as output
def kernel(p):
    hist = list(range(10))
    x = np.array([i * 1 / len(hist) for i in hist])
    d = np.argmin(abs(x - p)) # return jump distance
    return d

# Parameters
''' LIFE TABLE '''
try:
    df = pd.read_csv(path + 'data' + os.sep + 'life_table.csv')
except:
    print('COULD NOT FIND LIFE TABLE. Exiting program...')
    sys.exit(1)

# df['px'][0:8] = [1] * 8
df['px'] = [1, 0.61, 0.81, 0.81, 0.81, 0.81,
            0.81, 0.81, 0.81, 0.81, 0.81,
            0.81, 0.81, 0.81, 0.81, 0]

# Number of different runs to average results
n_runs = 100
run_parallel = True

'''
POSSIBLE (DISTINCT) DISPERSAL STRATEGIES (?)
'''

