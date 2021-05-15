from PSO import PSO
from GA import GA
from Solution import Solution
import random

"""
The manager class. Stores solutions, calls GA and PSO, and
passes results back to the interface
"""

class Driver(object):

	solutions = []
	clauses = []
	ga = GA()
	pso = PSO()

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

	def __init__(self, file_name, pop_size):
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
			if (solution.bitString[abs(int(literal)) - 1] != good_value):
				return False
			return True

	"""Given a set of problems and an Individual solution object, determines the fitness
	score of that Individual. Returns the updated fitness score as an int.
	"""
	def test_eval(self, lines, solution):
		for line in lines:
			literals_list = line.split()
			if (self.check_score(solution, literals_list)):
				solution.fitness += 1
		return solution.fitness

	"""Helper to allow sorting of solutions based on their fitness values.
	Takes an Individual object as an argument, returns that Individual's fitness
	which is an int value.
	"""
	def rankSort(self, individual):
		return individual.fitness

	#TODO - re-evaluate fitness and update at the start of every iteration
	def iterate(self):
		new_solutions = ga.process(self.solution[0, math.floor(len(solutions)/2)])
		new_solutions = pso.process(new_solutions)
		new_solutions.append(pso.process(self.solution[math.floor(len(solutions)/2), :-1]))
		self.solutions = new_solutions.copy()
		self.solutions.sort(key=self.rankSort)
		return self.solutions[0]
