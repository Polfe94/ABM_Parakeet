import random
import math
import numpy as np
from copy import deepcopy
import params

'''
PARAKEET AGENT 
'''
kernel = params.kernel

class Parakeet():
	
	def __init__(self, age, pos = None, coords = (0, 0), dispersal = 'jump'):

		self.age = age
		
		if pos is None:
			# Position, state and rates initialization
			if params.start_node == 'center':
				x, y = int(params.width / 2), int(params.height / 2)
			else:
				x, y  = random.randrange(params.width), random.randrange(params.height)
		else:
			x, y = pos

		self.pos = (x, y)
		self.coords = coords
		self.probabilities = {'px': params.df['px'][self.age],
					'mx': params.df['mx'][self.age]}
  
		# Dispersal movement
		self.move = self.choose_dispersal_strategy(dispersal)


	# Pick the appropriate dispersal strategy for parakeets
	def choose_dispersal_strategy(cls, dispersal):

		if dispersal == 'jump':
			return cls.dispersal_jump

		elif dispersal == 'moore':
			return cls.dispersal_moore

		elif dispersal == 'neumann':
			return cls.dispersal_neumann

	def update_probabilities(self):
		k = list(self.probabilities.keys())
		for p in k:
			self.probabilities[p] = params.df[p][self.age]


	''' MOVEMENT FUNCTIONS '''
	# Border effect (repulsion)
	def dispersal_jump(self, grid):
		prev_pos = self.pos

		# dispersion parameters 
		alpha = 2 * math.pi * random.random() # angle
		d = kernel() # distance
		r = d / grid.scale # distance in meters to pixels in grid

		# new position
		x, y = r * math.cos(alpha) + self.pos[0], r * math.sin(alpha) + self.pos[1]
		self.coords = x, y
		xy = np.array([(x, y)])

		# compute Euclidean distances
		closest_cell = np.linalg.norm(np.array(grid.coords) - xy, axis=1)
		minxy = np.where(closest_cell == min(closest_cell))[0]
		self.pos = grid.coords[int(minxy)]

		# update move in the grid
		grid.grid[prev_pos] -= 1
		grid.grid[self.pos] += 1
  
		# return (d, alpha)

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
	
 
	''' POSSIBLE ACTIONS '''
	def die(self, grid):
		grid.grid[self.pos] -= 1

	def mate(self, grid):
		# Note that there is a probability of non-mating at all
		n = random.randrange(3) # number of individuals // REPLACE
		# n = 5
		grid.grid[self.pos] += n
		return n

	def grow(self):
		self.age += 1

	''' ACTION CHOICE '''
	def action(self, grid):

		# returns boolean (is the agent still alive?) and integer (newborn parakeets)

		if random.random() > self.probabilities['px']:
			self.die(grid)
			return False, 0
			# return False, 0, 0, 0

		if self.age < params.adulthood:
			newborns = 0
			# d = 0
			# alpha = 0

		else:
			if random.random() <= self.probabilities['mx']:
				self.move(grid)
				# d, alpha = self.move(grid)
				newborns = self.mate(grid)

			else:
				newborns = 0
				# d = 0
				# alpha = 0

		self.grow()
		self.update_probabilities()

		return True, newborns#, d, alpha
