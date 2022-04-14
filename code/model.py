import numpy as np
from agent import *
import params
import pandas as pd
from collections import Counter
from itertools import compress
from copy import deepcopy

class DeterministModel:

	def __init__(self, agents, environment, init_pos = None):

		self.agents = agents
		self.environment = environment
		self.life_table = params.df
		if init_pos is None:
			self.init_pos = self.agents[0].pos

		self.environment.grid[self.init_pos] = len(self.agents)

		self.df = pd.DataFrame({'x': [self.agents[0].pos[0]],
		'y': [self.agents[0].pos[1]],
		't': [0],
		'n': [len(self.agents)]})

		# visualization gif
		self.frames = [self.environment.grid]

	def population_metrics(self):
		pass
	
	def step(self, key):

		pos = []
		d_idx = []
		births = []

		for a in self.agents:

			death, newborns = a.action(self.environment)
			d_idx.append(death)
			for i in range(newborns):
				births.append(Parakeet(0, pos = a.pos))
			
			pos.append(a.pos)

		self.agents = list(compress(self.agents, d_idx))
		self.agents.extend(deepcopy(births))
		c = Counter(pos)
		df = pd.DataFrame([[x[0], x[1], key, c[x]] for x in c],
		columns= ['x', 'y', 't', 'n'])
		self.df = self.df.append(df)
		upos = list(set(pos)) # unique positions
		if len(upos) > 1:
			maxd = max(abs(np.linalg.norm(np.array(upos) - self.init_pos, axis = 1)))

		else:
			maxd = 0.0

		return len(self.agents), maxd

	def save_data(self, path, filename):
		self.df.to_csv(path + filename + '.csv')
		self.result.to_csv(path + filename + '.csv')

	def run(self, steps):

		d = {'t': [0], 'n': [len(self.agents)], 'r': [0]}
		for i in range(steps):
			a, r = self.step(i + 1)
			d['t'].append(i)
			d['n'].append(a)
			d['r'].append(r)
			self.frames.append(self.environment.grid)

		self.result = pd.DataFrame(d)

