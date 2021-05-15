#Driver file
from Driver import Driver
import sys
import random
import time

def main():

    #setup
    #TODO: what parameters will we be passing?
    file_name = ""
    system = ""
    num_ants = 0
    iterations = 1000
    phero_influ = 0
    heuristic_influ = 0
    evap_fac = 0
    elitism_fac = 0
    """
    if len(sys.argv) == 1:
        print ("Please select a file")
        file_name = str(input())
        print ("Please select an ant system from the following: basic, elitist, best_worst, or rank")
        system = str(input())
        print ("Please input desired number of ants")
        num_ants = int(input())
        print ("Please input desired number of iterations")
        iterations = int(input())
        print ("Please input a desired phermone influence")
        phero_influ = float(input())
        print ("Please input a desired heuristic influence")
        heuristic_influ = float(input())
        print ("Please input a desired phermone evaportation factor")
        evap_fac = float(input())

    else:
        system = str(sys.argv[2])
        num_ants = int(sys.argv[3])
        iterations = int(sys.argv[4])
        phero_influ = float(sys.argv[5])
        heuristic_influ = float(sys.argv[6])
        evap_fac = float(sys.argv[7])
        elitism_fac = float(sys.argv[8])
    """
    file_name = str(sys.argv[1])
    driver = Driver(file_name, 16, "vn", "b")
    #everything here down should pretty much stay the same
    for iteration in range(iterations):
        driver.iterate()
        if iteration % 50 == 0:
            print("Iteration: "+str(iteration)+" Best Fit: "+str(driver.bestFit))

if __name__ == '__main__':
    main()
