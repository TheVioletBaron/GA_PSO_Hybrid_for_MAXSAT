import math
import random
"""
Stores a single solution, with methods for retrival and manipulation
"""

class Solution(object):

	def __init__(self, input):
		print(input)


		#BestFits for all solutions will be updated every iter in case a GA solution gets put in the PSO group
		self.pbest = math.inf #best value Particle has received from eval func
		self.bestPos = [] #Holds solution list of best solution found by particle
		#Variables below will only be used when a solution is in PSO group
		self.neighborhood = [] #List of all solutions in neighborhood
		self.nBestPos = [] #Holds solution vector of best solution in neighborhood
		self.nBest = math.inf #Fitness of best solution in neighborhood


	#The Particle update mathod will be added but only called for the 2N solutions in PSO