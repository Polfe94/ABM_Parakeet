import sys
import os
from unittest import result

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import params 
from agent import *
from lattice import Lattice
from model import *


import numpy as np
import math
import time
import random
import pandas as pd

from copy import deepcopy

from argparser import argparse

# argument parser to change parameters from the command line (or a bash script)
argparse(sys.argv[1:])

result_path = params.result_path
filename = params.file_name

if os.path.exists(result_path + filename + '.csv'):
	filename = filename + '_' + str(random.random())
	print('+++ Result file already exists! Changing name to avoid override... +++')

def create_instance(n_agents, n, agent = Parakeet(params.starting_age)):
	instances = []
	for i in range(n):
		environment = deepcopy(Lattice(params.width, params.height))
		instances.append(deepcopy(DeterministModel([agent] * n_agents, environment)))
	return instances

if not os.path.isdir(result_path):
	os.mkdir(result_path)

if params.n_runs > 1:
	os.mkdir(result_path + filename)

	if params.run_parallel:

		def run_parallel(model):
			random.seed(random.randrange(99999) * random.random() + time.time())
			model.run()
			return deepcopy(model)
		
		models = create_instance(params.n_agents, params.n_runs)

		import multiprocessing as mp
		pool = mp.Pool(mp.cpu_count())
		models = pool.map(run_parallel, models)
		pool.join()
		pool.terminate()

		for i in range(len(models)):
			models[i].save_data(result_path, + os.sep + filename + filename + '_' + str(i))

	else:
		models = []
		for run in range(params.n_runs):
			model = create_instance(params.n_agents, params.n_runs)[0]
			random.seed(time.time())
			print(model.environment.food)
			model.run()
			model.data2json(folder = filename + '/', filename = filename + '_' + str(run),
			 get_pos = params.retrieve_positions)
			models.append(model)

	# AVERAGE DATAFRAME FOR THE RESULTS
	# mrg = merge_runs(models) # single data frame for all results
	# avg, sd = average_runs(mrg)
	# avg.to_csv(folder + filename + '_average.csv')
	# sd.to_csv(folder + filename + '_sd.csv')

else:
	model = create_instance(1)[0]
	model.run()
	model.data2json(filename = filename, get_pos = params.retrieve_positions)