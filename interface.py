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
    iterations = 10000
    phero_influ = 0
    heuristic_influ = 0
    evap_fac = 0
    elitism_fac = 0
    
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
        file_name = str(sys.argv[1])
        populaion = int(sys.argv[2])
        topology = str(sys.argv[3])
        selection_method = str(sys.argv[4])
        mut_prob = float(sys.argv[5])

    driver = Driver(file_name, populaion, topology, selection_method, mut_prob)

    output = open("output.csv", "a")
    output.write("#" + file_name + "," + str(populaion) + "," + str(topology) + "," + str(phero_influ) + "," + str(selection_method) + "," + str(mut_prob))
    start = time.time()
    for iteration in range(iterations):
        driver.iterate()
        if iteration % 50 == 0:
            print(driver.bestFit)
            output.write(str(iteration) + "," + str(time.time() - start) + "," + str(driver.bestFit) +"\n")
        if (time.time() - start) > 300:
            print("Timed out")
            output.write("Timed Out")
            break


if __name__ == '__main__':
    main()
