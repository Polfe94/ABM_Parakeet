import os
import pandas as pd
from scipy.optimize import brentq as root
import math
import random

path = os.path.dirname(os.path.dirname(__file__)) + os.sep
result_path = path + 'results' + os.sep
file_name = 'test' 

adulthood = 1 # age of sexual maturity
max_dispersal_age = 1 # maximum age of dispersal


""" DISPERSAL DISTRIBUTION """
def pdoubleexp_trans(x, beta = 0.000499, lambda1 = 0.000387, lambda2 = 0.009626, xmin = 13, xmax = 28578):
    
    u = random.random()
    
    temp1= beta*((1+lambda1*xmin)/(lambda1*lambda1))*math.exp(-lambda1*xmin) - beta*((1+lambda1*xmax)/(lambda1*lambda1))*math.exp(-lambda1*xmax)
    temp2= (1-beta)*((1+lambda2*xmin)/(lambda2*lambda2))*math.exp(-lambda2*xmin) - (1-beta)*((1+lambda2*xmax)/(lambda2*lambda2))*math.exp(-lambda2*xmax)
    tempX1= beta*((1+lambda1*xmin)/(lambda1*lambda1))*math.exp(-lambda1*xmin) - beta*((1+lambda1*x)/(lambda1*lambda1))*math.exp(-lambda1*x)
    tempX2= (1-beta)*((1+lambda2*xmin)/(lambda2*lambda2))*math.exp(-lambda2*xmin) - (1-beta)*((1+lambda2*x)/(lambda2*lambda2))*math.exp(-lambda2*x)
    p=(tempX1+tempX2)/(temp1+temp2)
    p-u

    return p-u

# double exponential (2D) using trascendental equation
def r2Dtrans(pdf = pdoubleexp_trans):
       
    out = root(pdf, a = 13, b = 28578, full_output=False, xtol = 1e-15)
    
    return out

""" PARAKEET ACTION'S PROBABILITIES """
try:
    df = pd.read_csv(path + 'data' + os.sep + 'life_table.csv')
    
except:
    print('COULD NOT FIND LIFE TABLE. Switching to default values...')
    df = pd.DataFrame({'age': list(range(16)),
                   'px': [1, 0.6] + [0.8] * 13 + [0],
                   'mx': [0, 0, 0.6] + [0.8] * 6 +[0.6, 0.4, 0.2] + [0] * 4,
                   'ma': [0, 1.05, 1.47, 1.58] + [1.47] * 8 + [0] * 4})

try:
    lays = pd.read_csv(path + 'data' + os.sep + 'parakeet_productivity.csv')

except:
    print('COULD NOT FIND EGG LAY TABLE. Switching to default values...')
    lays = pd.DataFrame({'Productivity': [0] * 76 + [1] * 23+
    [2] * 51 + [3] * 65 + [4] * 72 + [5] * 44 + [6] * 34 + [7] * 12 +
    [8] * 3 + [9] + [11], 'POSTA': [1] * 382})

lays_p = {'Values': list(set(lays['Productivity']))}
lays_p['Probabilities'] = [len(lays[lays['Productivity'] == i])/len(lays) for i in lays_p['Values']]

try:
    dispersals = pd.read_csv(path + 'data' + os.sep + 'dispersal.csv')
    dispersal_prob = [len(dispersals[dispersals['d'] == 0]) / len(dispersals)]
    dispersal_prob.append(1 - dispersal_prob[0])

except:
    print('COULD NOT FIND DISPERSAL DISTANCES. Switching to default values...')
    dispersal_prob = [0.3, 0.7]



