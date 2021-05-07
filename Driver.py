from PSO import PSO
from GA import GA
from Solution import Solution

"""
The manager class. Stores solutions, calls GA and PSO, and
passes results back to the interface
"""

class Driver(object):

	def __init__(self, input):
		print(input)

	def iterate(self):
		print("Iterating")
