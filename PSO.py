from Solution import Solution
from random import *
import math

class PSO(object):

#change to handle bitstrings
#Ring w/ house metaphor Neighborhhod
#Optional re-assigning neighborhood
#only pass back half of list


    DIMENSION_COUNT = 30
    PARTICLE_COUNT = 0

    particles = None #for now, will need a diff one depending on topology

    '''
    Beore writing Von Neumann, we need to add a way to specify num of dimensions and make sure it doesn't impact the rest of the program.
    '''
    def __init__(self):
        self.topology = "topology"
        self.DIMENSION_COUNT = 0#len(gaSolutions[0]) #For now just getting num_clauses
        self.PARTICLE_COUNT = 0#len(gaSolutions) + len(pSolutions)
        self.particles = []#gaSolutions + pSolutions
        self.ga_solutions = []#gaSolutions
        self.pSolutions = []#pSolutions
    
    def initialize_particles_global(self):
        #assign entire swarm as neighborhood after all particles created
        for i in range(0, len(self.pSolutions)):
            self.pSolutions[i].neighborhood = self.particles

    def initialize_particles_ring(self):
        #Does normal ring to find indeces but takes particles from GA_solution list
        for i in range(len(self.pSolutions)):
            sol = self.pSolutions[i]
            neighborhood = []
            left = i - 1
            right = i + 1

            #wrap around array
            if i == 0: #won't need 
                left =  -1
            if right > len(self.pSolutions) - 1:
                right = 0

            neighborhood.append(self.ga_solutions[left]) 
            neighborhood.append(self.ga_solutions[right]) 
            neighborhood.append(sol) 
            sol.neighborhood = neighborhood

    def initialize_particles_houses(self):
        for i in range(len(self.psolutions)):
            solution = self.pSolutions[i]
            if i == 0:
                left = -1
                right = i + 1
            elif i == range(len(self.psolutions))-1:
                left = i - 1
                right = 0
            else:
                left = i - 1
                right = i +1
            solution.neighborhood = []
            solution.neighborhood.append(solution)
            solution.neighborhood.append(self.pSolutions[left])
            solution.neighborhood.append(self.pSolutions[right])
            solution.neighborhood.append(self.ga_Solutions[left])
            solution.neighborhood.append(self.ga_Solutions[right])
            solution.neighborhood.append(self.ga_Solutions[i])

    def initialize_von_neuman(self): 
        row_len = 0
        col_len = 0
        if self.PARTICLE_COUNT == 16: 
            col_len = 4
            row_len = 4
        elif self.PARTICLE_COUNT == 30:
            col_len = 5
            row_len = 6
        elif self.PARTICLE_COUNT == 64:
            col_len = 8
            row_len = 8
        else:
            print("invalid swarm size for von Neumann")
            quit()

        row_counter = 0
        col_counter = 0
        particles_grid  = [[0]*col_len]*row_len
        merged = []
        for j in range(len(self.ga_solutions)):
            merged.append(self.ga_solutions[j])
            merged.append(self.pSolutions[j])
        for i in range(0, len(merged)):
            try:

                if row_counter < row_len:
                    particles_grid[row_counter][col_counter] = merged[i]
                    #self.particles.append(Particle(0,velocities,positions))
                    row_counter += 1
                else:
                    row_counter = 0
                    col_counter += 1
                    particles_grid[row_counter][col_counter] = merged[i]
                    #self.particles.append(Particle(0,velocities,positions))
            except IndexError:
                print("uh oh")

        for i in range(0, row_len):
            for j in range (0, col_len):
                left = i - 1
                if i == 0:
                    left = row_len - 1

                right = i + 1
                if i == row_len - 1:
                    right = 0

                up = j - 1
                if j == 0:
                    up = col_len - 1

                down = j + 1
                if j == col_len - 1:
                    down = 0
                try:
                    neighborhood = [particles_grid[left][j], particles_grid[right][j],
                        particles_grid[i][up], particles_grid[i][down], particles_grid[i][j]]
                    particles_grid[i][j].neighborhood = neighborhood

                except IndexError:
                    print("Aly's fault")

    def initialize_random(self, isSetup):
        num_neighbors = 10  #Setting neighborhood size to 10 for now, but maybe we should change this based on num particles? Good idea
        for i in range (0, len(self.pSolutions)):
            if isSetup: #or random.uniform(0, 1) <= 0.2:
                neighborhood = []
                neighborhood.append(self.pSolutions[i])
                neighbor_counter = 1

                while neighbor_counter < num_neighbors:
                    rand = randint(0, self.PARTICLE_COUNT)
                    if self.particles[rand] not in neighborhood:
                        neighborhood.append(self.particles[rand])
                        neighbor_counter += 1
                self.pSolutions[i].neighborhood = neighborhood
                
    def find_gBest(self, solution):
        for sol in solution.neighborhood:
            if sol.pBestFit > solution.nBestFit: 
                solution.nBestFit = sol.pBestFit
                solution.nBest = sol.bitString #Adding copy() fixed all errors

    #If we need to pass the lists of solutions
    def process(self, topology , gaSolutions, pSolutions):
        self.topology = topology
        #self.DIMENSION_COUNT = len(gaSolutions[0]) #For now just getting num_clauses
        self.PARTICLE_COUNT = len(gaSolutions) + len(pSolutions)
        self.particles = gaSolutions + pSolutions
        self.ga_solutions = gaSolutions
        self.pSolutions = pSolutions
         #Made only one iteration
        if self.topology == "gl": #global
            self.initialize_particles_global()
        if self.topology == "ri": #ring
            self.initialize_particles_ring()
        if self.topology == "ra": #random
            self.initialize_random(True)
        if self.topology == "houses":
            self.initialize_particles_houses()
        if self.topology == "vn":
            self.initialize_von_neuman

        for solution in self.pSolutions:
            self.find_gBest(solution)#update gbest dynamically
            solution.modifiedUpdate()#update particle
        return self.pSolutions
