import random
import math
import numpy as np
from copy import deepcopy
import params

'''
PARAKEET AGENT 
'''

class Parakeet():
	

	def __init__(self, age = 1, pos = (0, 0)):

		self.age = age
		self.pos = pos
		self.probabilities = {'px': params.df['px'][self.age],
					'mx': params.df['mx'][self.age]}
  
		# Dispersal movement
		self.move = self.dispersal_jump
		self.has_nested = False
		self.counted = False # counted for the area computation of dispersal

	def update_probabilities(self):
		k = list(self.probabilities.keys())
		for p in k:
			self.probabilities[p] = params.df[p][self.age]


	''' MOVEMENT FUNCTIONS '''
	def dispersal_jump(self, grid, kernel):
		prev_pos = self.pos

		# dispersion parameters 
		alpha = 2 * math.pi * random.random() # angle
		r = kernel() # distance

		# new position
		x, y = r * math.cos(alpha) + self.pos[0], r * math.sin(alpha) + self.pos[1]
  
		self.pos = round(x, 4), round(y, 4)

		# update move in the grid
		grid.coords[prev_pos] -= 1
		if self.pos in grid.coords:
			grid.coords[self.pos] += 1
		else:
			grid.coords[self.pos] = 1
 
	''' POSSIBLE ACTIONS '''
	def die(self, grid):
		grid.coords[self.pos] -= 1

	def mate(self, grid):
     
		# Note that there is a probability of non-mating at all
		n = np.random.choice([0, 1, 2], p= [0.1, 0.45, 0.45])
		grid.coords[self.pos] += n
		return n

	def grow(self):
		self.age += 1

	''' ACTION CHOICE '''
	def action(self, grid, kernel):

		# returns boolean (is the agent still alive?) and integer (newborn parakeets)

		if random.random() >= self.probabilities['px']:
			self.die(grid)
			return False, 0

		if self.age < params.adulthood:
			newborns = 0

  
		elif self.age <= params.max_dispersal_age:
      
			if not self.has_nested:
				dispersal = np.random.choice([False, True], p = params.dispersal_prob)
				if dispersal:
					# d, alpha = self.move(grid)
					self.move(grid, kernel)
					self.has_nested = True

			newborns = self.mate(grid)

		else:
			newborns = self.mate(grid)

		self.grow()
		self.update_probabilities()

		return True, newborns
