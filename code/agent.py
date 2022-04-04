import random
import math
import numpy as np
import networkx as nx
from copy import deepcopy

from networkx.algorithms.cluster import square_clustering
import params

'''
STATES AND TAGS
'''

class State():   
	
	REPRODUCING = 'R'
	COLONIZING = 'C'
	STAYING = 'S'
	GROWING = 'G'

'''
PARAKEET AGENT 
'''

class Parakeet():
	
	def __init__(self, unique_id, dispersal = 'jump'):

		# id initialization
		self.id = unique_id
		
		# Position, state and rates initialization
		if params.start_node == 'center':
			x, y = int(params.width / 2), int(params.height / 2)
		else:
			x, y  = random.randrange(params.width), random.randrange(params.height)

		self.pos = (x, y)
		self.state = 'S'
		self.r_i = params.df.iloc[-1]['age'] / 10 # ??

		self.rates = {'mu': 1 - params.df['px'][0],
					'gamma': 1,
					'beta': 0,
					'rho': 0}
  
		  # Dispersal movement
		self.move = self.choose_dispersal_strategy(dispersal)

		# Age tag
		self.age = -1 # new borns


	# Pick the appropriate dispersal strategy for parakeets
	def choose_dispersal_strategy(cls, dispersal):

		if dispersal == 'jump':
			return cls.dispersal_jump

		elif dispersal == 'moore':
			return cls.dispersal_moore

		elif dispersal == 'neumann':
			return cls.dispersal_neumann

	def update_rates(self):
		self.rates['mu'] = params.df['px'][self.age]
		self.rates['gamma'] = 0
		self.rates['beta'] = 1
		self.rates['rho'] = params.df['mx'][self.age]
		self.r_i = sum(self.rates.values())

	# Border effect (repulsion)
	def dispersal_jump(self, grid):
		prev_pos = self.pos
		alpha = 2 * math.pi * random.random()

		## replace with a dispersal kernel !!!!!!!
		r = random.randrange(int(params.width * .2)) 
		r += random.random()
		# new position
		x, y = r * math.cos(alpha) + self.pos[0], r * math.sin(alpha) + self.pos[1]
		xy = np.array([(x, y)])

		# compute Euclidean distances
		closest_cell = np.linalg.norm(np.array(grid.coords) - xy, axis=1)
		minxy = np.where(closest_cell == min(closest_cell))[0]
		self.pos = grid.coords[int(minxy)]

		# update move in the grid
		grid.grid[prev_pos[0]][prev_pos[1]] -= 1
		grid.grid[self.pos[0]][self.pos[1]] += 1

	# def dispersal_jump(self):
	#     alpha = 2 * math.pi * random.random()
	#     r = random.randrange(int(params.width * .2)) ## replace with a dispersal kernel
	#     r += random.random()
	#     x, y = r * math.cos(alpha) + self.pos[0], r * math.sin(alpha) + self.pos[1]
	#     self.pos = (round(x), round(y))
	
	def dispersal_moore(self, grid):
		pass

	def dispersal_neumann(self, grid):
		pass
	
 
	def die(self, grid):
		grid.grid[self.pos[0]][self.pos[1]] -= 1
		self.r_i = 0
	
	def mate(self, grid):
		n = random.randrange(3, 5) # number of individuals // REPLACE
		grid.grid[self.pos[0]][self.pos[1]] += n
		return n

	def grow(self):
		self.age += 1

	def stay(self):
		self.state = 'S'



	# Possible actions the parakeet may take, based on state
	def action(self, grid):
	 
		self.grow()

		if self.age == 0:
			newborns = 0
			
		else:

			if random.random() < self.mu:
				self.die()
				newborns = 0

			else:
					
				if self.age >= params.adulthood:
					self.move(grid)
					newborns = self.mate(grid)

		return newborns
