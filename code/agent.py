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

class Tag():

	ADULT = 1 # More than 3 years
	YOUNG = 0 # Less or equal than 3 years

'''
PARAKEET AGENT 
'''

class Parakeet():
	
	def __init__(self, unique_id, dispersal = 'jump'):

		# id initialization
		self.id = unique_id
		
		# Position, state and rates initialization
		self.pos = params.start_node
		self.state = 'S'
		self.prev_state = 'S'
		self.state_history = []
		self.r_i = 0
  
  		# Dispersal movement
		self.move = self.choose_dispersal_strategy(dispersal)

		# Age tag
		self.age = -1 # new borns
		self.tag = Tag.YOUNG ## Tag.ADULT ? ## int(round(random.random()))

	# Pick the appropriate dispersal strategy for parakeets
	def choose_dispersal_strategy(cls, dispersal):

		if dispersal == 'jump':
			return cls.dispersal_jump

		elif dispersal == 'moore':
			return cls.dispersal_moore

		elif dispersal == 'neumann':
			return cls.dispersal_neumann

	def dispersal_jump(self, grid):
		alpha = 2 * math.pi * random.random()
		distance = random.randrange(10) ## change
  
		# rotation to x axis
		x, y = self.pos[0] * math.cos(alpha), self.pos[1] + distance
		# compute Euclidean distances
		closest_cell = np.linalg.norm(grid.pos - (x, y), axis=1)
		minxy = np.where(min(closest_cell))[0]
		self.pos = grid.pos[int(minxy)]
	
	def dispersal_moore(self, grid):
		pass

	def dispersal_neumann(self, grid):
	 	pass
	
 
	def die(self):
		 pass

	def mate(self):
		pass

	def grow(self):
		self.age += 1
		if self.age == params.adulthood:
			self.tag = Tag.ADULT

	def stay(self):
		pass



	# Possible actions the parakeet may take, based on the position and the state
	# returns true if food is found and picked up
	# this value is fed into the gillespie algorithm
	def action(self):
     
		self.grow()
	 
		if self.tag == Tag.YOUNG:
			if self.age == 0:
				self.stay()
		
		else:
			self.move()
