from Solution import Solution

"""
Authors: Aly Hummel
Date 12 May 2021
Course: Nature Inspired Computation
File Description: This file holds the GA class which takes in certain arguments (a file of MAXSAT problems 
+ a number of variables dictating the variable settings for running the GA algorithm on them). The class
runs the algorithm and has the ability to output the best possible solutions.
"""
import random
from math import *
import sys
import time

class GA(object):
    
    solution_list = []
    mut_prob = 0.01 #hard coded for now

    """Initiializing function for the GA class. Function is used to generate a GA object.
    """
    def __init__(self, mut_prob):
        self.mut_prob
    
    """Iterates through the Individual solutions and probabilistically mutates on a randomly
    selected bit in the Individual's bitstring.
    """
    def mutate(self):
        for individual in self.solution_list:
            for i in range (0, len(individual.bitString)):
                rand = random.random()
                if rand < self.mut_prob:
                    new_bit = "0" if individual.bitString[i] == "1" else "1"
                    individual.bitString = individual.bitString[:i] + new_bit + individual.bitString[i + 1:]
    
    """To help with crossing over, randomly selects two Individuals from the solution
    list, ensuring that they are different, and then returns the Individual objects.
    """
    def choose_parents(self):
        pos1 = random.randint(0, (len(self.solution_list) - 1))
        parent1 = self.solution_list[pos1]
        pos2 = random.randint(0, (len(self.solution_list) - 1))
        parent2 = self.solution_list[pos2]
        while pos2 == pos1: #If parents are the same object, finds a new second parent
            if len(self.solution_list) == 1:
                return parent1, parent1
            pos2 = random.randint(0, (len(self.solution_list) - 1))
            parent2 = self.solution_list[pos2]
        return parent1, parent2

    """Given a string representing a crossover method as an argument, crosses over
    until a new breeding pool of the correct size i.e. the original population
    size is achieved. Depending on the crossover method provided, makes a
    function call to aquire those two children to add.
    """    
    def crossover(self):
        new_breeding_pool = []
        new_pop = 0
        total_pop = len(self.solution_list)
        while new_pop < total_pop:
            child1, child2 = self.one_point_crossover()
            new_breeding_pool.append(child1)
            if total_pop - new_pop != 1:
                new_breeding_pool.append(child2)
                new_pop += 2
            else:
                new_pop += 1
        self.solution_list = new_breeding_pool

    """Performs one-point crossover, choosing two parents, randomly selecting a crossover
    point that does not include the first or last variables of a bitstring, and then
    crosses over between the two parents at that point (swaps bitstrings after the
    stated point). Returns two child Individual objects.
    """
    def one_point_crossover(self):
        var_num = len(self.solution_list[0].bitString)
        parent1, parent2 = self.choose_parents()
        self.solution_list.remove(parent1)
        if parent1 != parent2:
            self.solution_list.remove(parent2)
        crossover_point = random.randint(1, var_num - 2) #don't choose last or first positions
        child1_string = parent1.bitString[0:crossover_point] + parent2.bitString[crossover_point:]
        child2_string = parent2.bitString[0:crossover_point] + parent1.bitString[crossover_point:]
        child1 = Solution(0, child1_string)
        child2 = Solution(0, child2_string)
        return child1, child2

    """Executes the crossove, and mutation calls on a GA object, returning the updated population. 
    """
    def process(self, solutions):
        self.solution_list = solutions
        self.crossover()
        self.mutate()
        return self.solution_list