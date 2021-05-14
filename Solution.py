import math
import random

class Solution:

    def __init__(self, fitness, bitString):
        self.fitness = fitness
        self.bitString = bitString
	    #BestFits for all solutions will be updated every iter in case a GA solution gets put in the PSO group
        self.fitness = 0 #Current fitness
        self.pBestFit = 0 #best value Particle has received from eval func
        self.pBest = "" #Holds solution list of best solution found by particle
	    #Variables below will only be used when a solution is in PSO group
        self.neighborhood = [] #List of all solutions in neighborhood
        self.nBest = "" #Holds solution vector of best solution in neighborhood
        self.nBestFit = 0 #Fitness of best solution in neighborhood

    #TODO: change to handle bitstrings
    def modifiedUpdate(self): 
        try:
            for i in range(0, len(self.bitString)):
                prob = random.uniform(0, 2.05)*math.abs(int(self.pBest[i]) - int(self.bitString[i])) + random.uniform(0, 2.05)*math.abs(int(self.nBest[i]) - int(self.bitString[i]))
                if prob < 1.025:
                    if self.bitString[i] == '1':
                        self.bitString[i] = '0'
                    else: self.bitString[i] = '1'

        except IndexError:
            print("Particle length incorrect")
            exit()

    #TODO: change to handle bitstrings
    def update(self): 
        try:
            for i in range(0, len(self.bitString)):
                newVelocity = 0.7298 * (self.bitString[i] + random.uniform(0, 2.05)*(self.pBest[i] - self.bitString[i]) + random.uniform(0, 2.05)*(self.nBest[i] - self.bitString[i]))
                self.velocity[i] = newVelocity
                self.positions[i] += self.velocity[i]
        except IndexError:
            print("Particle length incorrect")
            exit()