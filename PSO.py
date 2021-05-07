from random import *
import math
import statistics

class Swarm(object):

    DIMENSION_COUNT = 30
    PARTICLE_COUNT = 0

    particles = None #for now, will need a diff one depending on topology

    '''
    Beore writing Von Neumann, we need to add a way to specify num of dimensions and make sure it doesn't impact the rest of the program.
    '''
    def __init__(self, topology, particle_count, opt, iterations):
        self.iterations = iterations
        self.PARTICLE_COUNT = particle_count
        self.eval = opt
        self.topology = topology
        if self.topology != "n": #neumann #TODO: worry about later
            self.initialize_particles() #Dont do for Vneumann
        if self.topology == "gl": #global
            self.initialize_particles_global()
        if self.topology == "ri": #ring
            self.initialize_particles_ring()
        if self.topology == "ra":  #random
            self.initialize_random(True)

        
        self.iterate()
        
    #All 3 function evaluations are passed a particle and will either return fitness, assign it to the particle, or both 

    #Rosenbrock working
    #(1 to d-1) sum {100 * (x[i+1] - x[i]^2)^2 + (x[i] - 1)^2}
    def rosenbrock(self, part):
        totalFit = 0
        for i in range(len(part.positions)-1):
            totalFit += 100 * pow(part.positions[i+1] - part.positions[i]**2, 2.0) + pow(part.positions[i]-1.0,2)
        return totalFit

    #Ackley Working
    def ackley(self, part): #Could use help checking if function is correct
        firstVal = 0.0
        secondVal = 0.0
        for i in range(len(part.positions)):
            firstVal += math.pow(part.positions[i], 2) #Calculates firstSum
            secondVal += math.cos(2.0 *math.pi*part.positions[i]) #Calculates secondSum
        finalFit = -20.0 * math.exp(-0.2 * math.sqrt(firstVal / len(part.positions))) - math.exp(secondVal / len(part.positions)) + 20.0 + math.e
        return finalFit
    
    #Rastrigin working, PSO gets amazing results
    #(1 to d) sum {x[i]^2 - 10*Cos(2*n*x[i]) + 10}
    def rastrigin(self, part):
        totalFit = 0
        for i in range(len(part.positions)):
            totalFit += math.pow(part.positions[i],2) - 10*math.cos(2*math.pi*part.positions[i]) + 10
        return totalFit

    #sphere working, but we should ask majercik about pmin,pmax,etc... in init_particles()-Line 80
    def sphere(self, part):
        sumSquares = 0
        for i in range(len(part.positions)):
            sumSquares += part.positions[i] ** 2
        return sumSquares
    
    #sets positions and velocity bounds for each evaluation function
    def initialize_particles(self):
        self.particles = []
        if self.eval == "rok": #Rosenbrock
            pmin = 15.0
            pmax = 30.0
            vmin = -2.0
            vmax = 2.0
        elif self.eval == "ack": #Ackley
            pmin = 16.0
            pmax = 32.0
            vmin = -2.0
            vmax = 4.0
        elif self.eval == "sp": #Sphere, Ask Prof Maj what initial values should be
            pmin = 15.56
            pmax = 25.12
            vmin = -2.0
            vmax = 4.0
        elif self.eval == "ras": #Rastrigin
            pmin = 2.56
            pmax = 5.12
            vmin = -5.0
            vmax = 4.0
        else:
            print("Argument Error: " + self.eval + " is not a function")
            exit()
        if self.topology == "vn":
            self.initialize_von_neuman(pmin, pmax, vmin, vmax)
        else:
            for i in range(0, self.PARTICLE_COUNT):
                positions = [] #randomly generate positions array
                velocities = [] #randomly generate velocities array
                for j in range(0, self.DIMENSION_COUNT): #Based on values specified by eval func
                    randp = random.uniform(pmin, pmax)
                    positions.append(randp)
                    randv = random.uniform(vmin, vmax)
                    velocities.append(randv)
                self.particles.append(Particle(0,velocities,positions))
        
    def initialize_particles_global(self):
        #assign entire swarm as neighborhood after all particles created
        for i in range(0, self.PARTICLE_COUNT):
            self.particles[i].neighborhood = self.particles

    def initialize_particles_ring(self):
        #assign entire swarm as neighborhood after all particles created
        for i in range(0, self.PARTICLE_COUNT):
            neighborhood = []
            left = i - 1
            right = i + 1

            #wrap around array
            if i == 0:
                left = len(self.particles) - 1
            if i == len(self.particles) - 1:
                right = 0

            neighborhood.append(self.particles[left]) 
            neighborhood.append(self.particles[right]) 
            neighborhood.append(self.particles[i]) 
            self.particles[i].neighborhood = neighborhood


    def initialize_von_neuman(self, pmin, pmax, vmin, vmax): #TODO
        row_len = 0
        col_len = 0
        if self.PARTICLE_COUNT == 16:
            col_len = 4
            row_len = 4
        elif self.PARTICLE_COUNT == 30:
            col_len = 5
            row_len = 6
        elif self.PARTICLE_COUNT == 49:
            col_len = 7
            row_len = 7
        else:
            print("invalid swarm size for von Neumann")
            quit()

        #initialize self.particles 2d array
        row_counter = 0
        col_counter = 0
        particles_grid  = [[0]*col_len]*row_len
        self.particles = []
        for i in range(0, self.PARTICLE_COUNT):
            positions = [] #randomly generate positions array
            velocities = [] #randomly generate velocities array
            
            for j in range(0, self.DIMENSION_COUNT): #Based on values specified by eval func
                randp = random.uniform(pmin, pmax)
                positions.append(randp)
                randv = random.uniform(vmin, vmax)
                velocities.append(randv)
            try:

                if row_counter < row_len:
                    particles_grid[row_counter][col_counter] = Particle(0,velocities,positions)
                    #self.particles.append(Particle(0,velocities,positions))
                    row_counter += 1
                else:
                    row_counter = 0
                    col_counter += 1
                    particles_grid[row_counter][col_counter] = Particle(0,velocities,positions)
                    #self.particles.append(Particle(0,velocities,positions))
            except IndexError:
                print("uh oh")

        # #initialize random positions
        # for i in range(0, self.PARTICLE_COUNT):
        #     #randomly generate positions array
        #     positions = []
        #     for j in range(0, self.DIMENSION_COUNT):
        #         rand = random.randrange(0, 100)
        #         positions.append(rand)
        
        #assign neighborhoods
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
                    self.particles.append(particles_grid[i][j])

                except IndexError:
                    print("Aly's fault")

    def initialize_random(self, isSetup):
        num_neighbors = 10  #Setting neighborhood size to 10 for now, but maybe we should change this based on num particles? Good idea
        for i in range (0, self.PARTICLE_COUNT):
            if isSetup or random.uniform(0, 1) <= 0.2:
                neighborhood = []
                neighborhood.append(self.particles[i])
                neighbor_counter = 1

                while neighbor_counter < num_neighbors:
                    rand = randint(0, self.PARTICLE_COUNT-1)
                    if self.particles[rand] not in neighborhood:
                        neighborhood.append(self.particles[rand])
                        neighbor_counter += 1
                self.particles[i].neighborhood = neighborhood
        
    #Calls evaluate func and only stores value when it is better than previous pBest of Particle
    def evaluate_particle(self,particle):
        if self.eval == "rok":
            score = self.rosenbrock(particle)
            if score < particle.pbest:
                particle.pbest = score
                particle.bestPos = particle.positions
        elif self.eval == "ack":
            score = self.ackley(particle)
            if score < particle.pbest:
                particle.pbest = score
                particle.bestPos = particle.positions
        elif self.eval == "sp":
            score = self.sphere(particle)
            if score < particle.pbest:
                particle.pbest = score
                particle.bestPos = particle.positions
        else: # when eval == "ras"
            score = self.rastrigin(particle)
            if score < particle.pbest: 
                particle.pbest = score
                particle.bestPos = particle.positions
    
    def find_gBest(self, particle):
        for part in particle.neighborhood:
            if part.pbest < particle.nBest: 
                particle.nBest = part.pbest
                particle.nBestPos = part.positions.copy() #Adding copy() fixed all errors


    def iterate(self):
        output = open("output.csv", "a")
        output.write("#" + self.topology + "," + str(self.PARTICLE_COUNT) + "," + self.eval + "," + str(self.iterations) + "\n")
        bests = []
        bestFit = math.inf  #Change to 0 if we want high values from eval function
        for particle in self.particles:
            self.evaluate_particle(particle) #find initial value and initial pBest for all particles       
        for i in range(0, self.iterations):
            for particle in self.particles:
                self.find_gBest(particle)#update gbest dynamically
                #print(particle.nBestPos)
                particle.update()#update particle
                self.evaluate_particle(particle) #update pbest
                if particle.pbest < bestFit:  #Change to > if we want high values from eval function
                    bestFit = particle.pbest
                    
            if self.topology == "ra":  #random, re-does neighborhoods, will need to do for ring and VN as well
                self.initialize_random(False)
            bests.append(bestFit)
            if (i+1) % 1000 == 0:
                    output.write(str(i) + "," + str(statistics.mean(bests)) + "," +str(statistics.median(bests)) + "\n") 
        print("Program terminated with no errors")
