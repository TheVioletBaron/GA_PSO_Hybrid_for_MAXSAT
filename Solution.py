class Solution:
    fitness = 0
    bitString = ""
    probability = 0
    def __init__(self, fitness, bitString):
        self.fitness = fitness
        self.bitString = bitString
	#BestFits for all solutions will be updated every iter in case a GA solution gets put in the PSO group
	self.pbest = math.inf #best value Particle has received from eval func
	self.bestPos = [] #Holds solution list of best solution found by particle
	#Variables below will only be used when a solution is in PSO group
	self.neighborhood = [] #List of all solutions in neighborhood
	self.nBestPos = [] #Holds solution vector of best solution in neighborhood
	self.nBest = math.inf #Fitness of best solution in neighborhood

    def setProb(self, newProbability):
        self.probability = newProbability
