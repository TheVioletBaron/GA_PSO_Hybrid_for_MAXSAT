import math
import random

class Solution:

    def __init__(self, fitness, bitString):
        self.fitness = fitness
        self.bitString = bitString
	    #BestFits for all solutions will be updated every iter in case a GA solution gets put in the PSO group
        self.fitness = 0 #Current fitness
        self.pBestFit = math.inf #best value Particle has received from eval func
        self.pBest = "" #Holds solution list of best solution found by particle
	    #Variables below will only be used when a solution is in PSO group
        self.neighborhood = [] #List of all solutions in neighborhood
        self.nBest = "" #Holds solution vector of best solution in neighborhood
        self.nBestFit = math.inf #Fitness of best solution in neighborhood

    #TODO: change to handle bitstrings
    def update(self): 
        try:
            for i in range(0, len(self.bitString)):
                newVelocity = 0.7298 * (self.velocity[i] + random.uniform(0, 2.05)*(self.bestPos[i] - self.positions[i]) + random.uniform(0, 2.05)*(self.nBestPos[i] - self.positions[i]))
                self.velocity[i] = newVelocity
                self.positions[i] += self.velocity[i]
        except IndexError:
            print("Particle length incorrect")
            exit()