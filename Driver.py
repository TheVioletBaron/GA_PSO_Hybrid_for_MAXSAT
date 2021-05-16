from PSO import PSO
from GA import GA
from Solution import Solution
import random
import math

"""
The manager class. Stores solutions, calls GA and PSO, and
passes results back to the interface
"""

class Driver(object):

	solutions = []
	clauses = []
	#ga = GA()
	pso = PSO()

	#for GA selection methods
	total_probability = 0
	sum_of_ranks = 0

	def generate_solutions(self, pop_size):
		for i in range(pop_size):
			bitString = ""
			for j in range(0, self.var_num):
				new_bit = str(random.randrange(0, 2))
				bitString = bitString + new_bit
			solution = Solution(0, bitString)
			self.solutions.append(solution)
		for solution in self.solutions:
			self.test_eval(self.clauses, solution)

	def __init__(self, file_name, pop_size, topology, selection_method, mut_prob):
		self.ga = GA(mut_prob)
		self.bestFit = 0
		self.topology = topology
		self.selection_method = selection_method
		self.readFile(file_name)
		solutions = self.generate_solutions(pop_size)
		self.solutions.sort(key=self.rankSort)
		

	"""Function handle file reading on the MAXSAT problem, handling the first comment lines
	before obtaining the number of variables, clauses, and finally grabbing the clauses
	themselves and storing those in a list.
	"""
	def readFile(self, file_name):
		f = open(file_name, "r")
		lines = f.readlines()
		while lines[0][0] == 'c':   #Remove beggining comment lines in file
			lines.remove(lines[0])
		first_line = lines[0].split() #Obtaining number of vairables and clauses
		self.var_num = int(first_line[2])
		self.clause_num = int(first_line[3])
		lines.pop(0)
		self.clauses = lines


	"""Function that takes an Individual solution and a given clause and checks
	if the solution satifies the clause. Returns a boolean.
	"""
	def check_score(self, solution, clause):
		for literal in clause[:-1]: #Needs to ignore the 0 at the end of each clause
			good_value = "1" if int(literal) > 0  else "0"
			if (solution.bitString[abs(int(literal)) - 1] == good_value):
				return True
		return False

	"""Given a set of problems and an Individual solution object, determines the fitness
	score of that Individual. Returns the updated fitness score as an int.
	"""
	def test_eval(self, lines, solution):
		solution.fitness = 0
		for line in lines:
			literals_list = line.split()
			if (self.check_score(solution, literals_list)):
				solution.fitness += 1
		if solution.pBestFit < solution.fitness:
			solution.pBestFit = solution.fitness
			solution.pBest = solution.bitString
		if solution.fitness  > self.bestFit:
			self.bestFit = solution.fitness
		return solution.fitness

	"""Helper to allow sorting of solutions based on their fitness values.
	Takes an Individual object as an argument, returns that Individual's fitness
	which is an int value.
	"""
	def rankSort(self, individual):
		return individual.fitness

	#all of the following are GA selection methods
	#they will select the half of the population that will go through GA processing
	#all remove GA pop from self.solutions and return GA pop in a separate list

	"""Function that executes rank selection on the pool of solutions by first ranking
    them by their fitness scores, and then selecting based on rank-based probailities
    until a pool equal in size to the original population has been made.
    """
	def rank_selection(self):
		self.total_probability = 0
		self.solutions.sort(key=self.rankSort)
		for i in range(0, len(self.solutions)): #Calculating each Individual's probability
			self.solutions[i].probability = (i + 1) / self.sum_of_ranks
			self.total_probability += self.solutions[i].probability
		return self.select_breeding_pool()

	"""Executes boltzmann selection by summing up all fitness scores
    as a denominator and then determining each Individual's probability. Selection occurs
    until a pool equal in size to the original population has been made.
    """
	def boltzmann_selection(self):
		self.total_probability = 0
		for i in range(0, len(self.solutions)): #Calculating each Individual's probability
			self.solutions[i].probability = math.exp(self.solutions[i].fitness/100) / self.sum_of_ranks
			self.total_probability += self.solutions[i].probability
		return self.select_breeding_pool()

	"""Executes exponential rank selection, calculating an indvidual's probability of
    being selected by taking e to the power of the individual's rank, and dividing
    that by the sum of e to the power of all the Inviduals' ranks. Calls method to
    do the actual selection.
    """
	def exponential_rank_selection(self):
		self.total_probability = 0
		self.solutions.sort(key=self.rankSort)
		for j in range(0, len(self.solutions)):
			self.solutions[j].probability = math.exp(j) / self.sum_of_ranks
			self.total_probability += self.solutions[j].probability
		return self.select_breeding_pool()

	"""Probabilistically selects Individuals and places them into the breeding
    pool until the pool is full i.e. equal to the size of the original population.
    Calculates a random float value which is used to find each Individual.
    """
	def select_breeding_pool(self):
		total_selected = 0
		#only selecting top half of total population
		half_pop = len(self.solutions) / 2
		selected = []
		while total_selected < half_pop:
			rand = random.uniform(0, self.total_probability)
			selected_ind = self.get_selected_individual(rand)
			selected.append(self.solutions[selected_ind])
			self.total_probability -= self.solutions[selected_ind].probability
			del self.solutions[selected_ind]
			total_selected += 1
		#self.solutions = []
		#self.solutions = selected
		return selected

	"""Given a random float value between 0 and the total of all the Individual
    probabilities calculated above, selects the indvidual who matches the random value.
    Returns an Individual object.
    """
	def get_selected_individual(self, random_number):
		prob_so_far = 0 #holds cumulative probabilties
		prev_individual = 0
		for i in range(0, len(self.solutions)):
			prob_so_far += self.solutions[i].probability
			if prob_so_far > random_number:
				return i
				#return (self.solutions[i])
			prev_individual += 1
		return i

	def iterate(self):
		ga_pop = []
		if self.selection_method == "b":
			for i in range (0, len(self.solutions) + 1): #Summing up total of ranks for later use
				self.sum_of_ranks += math.exp(self.solutions[i - 1].fitness/100)
			ga_pop = self.boltzmann_selection()
		if self.selection_method == "rs":
			for i in range (0, len(self.solutions) + 1): #Summing up total of ranks for later use
				self.sum_of_ranks += i
			ga_pop = self.rank_selection()
		if self.selection_method == "er":
			for i in range (0, len(self.solutions) + 1): #Summing up total of ranks for later use
				self.sum_of_ranks += math.exp(i)
			ga_pop = self.exponential_rank_selection()
		if self.selection_method =="r":
			self.solutions.sort(key=self.rankSort)
			ga_pop = self.solutions[0:math.floor(len(self.solutions)/2)]

		new_solutions = self.ga.process(ga_pop)

		#new_solutions = self.pso.process(new_solutions)
		#if used GA selection method, use separate pop lists
		# else, use indexing
		# TODO updating pBest here using test_eval, no idea if we want to keep doing this
		if self.selection_method == "r":
			pso_output = self.pso.process(self.topology, new_solutions, self.solutions[math.floor(len(self.solutions)/2):])
			#new_solutions.append(self.pso.process(self.topology, new_solutions, self.solutions[math.floor(len(self.solutions)/2):-1]))
		else:
			pso_output = self.pso.process(self.topology, new_solutions, self.solutions)
		
		new_solutions += pso_output
		
			#new_solutions.append(self.pso.process(self.topology, new_solutions, self.solutions))
		# new_solutions.append(self.pso.process(self.topology, new_solutions, self.solutions[math.floor(len(self.solutions)/2):-1]))
		self.solutions = new_solutions[:]

		#fitness evaluation
		for solution in self.solutions:
			self.test_eval(self.clauses, solution)

		# self.solutions.sort(key=self.rankSort)
		# return self.solutions[0]

	def proccess(self):
		print(self.get_best().fitness)
		ITERATIONS = 5 #hard coded for now
		for i in range(0, ITERATIONS):
			self.iterate()
			print(self.get_best().fitness)

	
	def get_best(self):
		max_solution = self.solutions[0]
		for sol in self.solutions:
			if sol.fitness > max_solution.fitness:
				max_solution = sol
		return max_solution
