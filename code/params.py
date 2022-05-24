import os
import sys
import pandas as pd
import numpy as np
from io import StringIO
import re
import subprocess
import math
import random

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

if width % 2 == 0:
    width += 1

if height % 2 == 0:
    height += 1


'''
POSSIBLE (DISTINCT) DISPERSAL STRATEGIES (?)
'''
# double exponential (2D)
def kernel():
    M = 0.000005590063 # function maximum
    beta = 0.0071277
    L1 = 0.00050245
    L2 = 0.00909844
    rmin = 1
    rmax = 3840

    d1 = beta * ((1 + L1 * rmin)/ L1 **2) * math.exp(-L1 * rmin)
    d2 = (1- beta) * ((1 + L2 * rmin) / L2 ** 2) * math.exp(-L2 * rmin)
    d3 = -beta *((1 + L1 * rmax) / L1 ** 2) * math.exp(-L1 * rmax)
    d4 = -(1- beta)* ((1+L2 * rmax) / L2 ** 2) * math.exp(-L2 * rmax)
     
    C = (1 / (2 * math.pi)) * (1 / (d1 + d2 + d3 + d4))
    
    while True:
        r = random.uniform(rmin, rmax)
        y = random.uniform(0, M)
        p = C * (beta * math.exp(-L1 * r) + (1 - beta)* math.exp(-L2 * r))
        if y < p:
            return r


# try:
#     p = subprocess.Popen('/usr/bin/Rscript --vanilla %sdoubleExp_sampling.R', shell = True, stdout = subprocess.PIPE)
#     p = str(p.stdout.read(), 'utf-8')
#     p = StringIO(p)
#     p = str(pd.read_csv(p))
#     p = re.sub(r'\[.*?\]', '', p)
#     p = p.split('')
#     p.remove('')

# except:
#     print('Something went wrong during kernel importation. Using default sampling distribution')


# Parameters
''' LIFE TABLE '''
try:
    df = pd.read_csv(path + 'data' + os.sep + 'life_table.csv')
    
except:
    print('COULD NOT FIND LIFE TABLE. Switching to default values...')
    df = pd.DataFrame({'age': list(range(16)),
                   'px': [1, 0.6] + [0.8] * 13 + [0],
                   'mx': [0, 0, 0.6] + [0.8] * 6 +[0.6, 0.4, 0.2] + [0] * 4,
                   'ma': [0, 1.05, 1.47, 1.58] + [1.47] * 8 + [0] * 4})

# Number of different runs to average results
n_runs = 100
run_parallel = True



