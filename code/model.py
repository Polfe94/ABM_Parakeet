import numpy as np
from agent import *
import pandas as pd
from itertools import compress
from copy import deepcopy

class DeterministModel:

	def __init__(self, agents, environment, kernel = params.r2Dtrans):

		self.agents = agents
		self.environment = environment
		self.births = []
		self.kernel = kernel

		self.frames = [deepcopy(self.environment.coords)]
		self.dispersion = []

	def population_metrics(self):
		pass
	
	def step(self):

		pos = []
		coords = []
		d_idx = []
		births = []

		for a in self.agents:

			death, newborns = a.action(self.environment, self.kernel)
			d_idx.append(death)
			for i in range(newborns):
				births.append(Parakeet(0, pos = a.pos))
    
			self.births.append(newborns) ## keep track of number of births
			if a.has_nested and not a.counted:
				pos.append(a.pos)
				a.counted = True

		self.agents = list(compress(self.agents, d_idx))

		self.dispersion.append(coords)

		self.agents.extend(deepcopy(births))

		if len(pos) > 0:
			meand = np.mean(abs(np.linalg.norm(np.array(pos) - (0, 0), axis = 1)))
		else:
			meand = 0
   
		return len(self.agents), meand

	def save_data(self, path, filename):
		self.result.to_csv(path + filename + '_result.csv')

  
	def compute_velocity(self):
		x, y = self.result['t'][1:], self.result['v'][1:]
		lm = np.polyfit(x, y, 1)
		return lm[0]

	def run(self, steps):

		d = {'t': [0], 'n': [len(self.agents)], 'r': [0], 'v': [0]}
		for i in range(steps):
			a, r = self.step()
			d['t'].append(i + 1)
			d['n'].append(a)
			d['r'].append(r)
			d['v'].append(math.sqrt(math.pi*(r**2)))
			self.frames.append(deepcopy(self.environment.coords))

		self.result = pd.DataFrame(d)

