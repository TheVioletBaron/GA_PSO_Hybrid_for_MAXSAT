#!/bin/bash

# Testing for GA-PSO Hybrid
#filename = "HG-3SAT-V250-C1000-7.cnf"
#baseline selection method: b
#baseline topology: ri
#baseline mut prob: 0.25

echo "TOPOLOGY TESTING"
for top in "gl" "ri" "vn" "ra" "houses" 
do
    for pop in 16 30 64 
    do
        python3 interface.py HG-3SAT-V250-C1000-7.cnf ${pop} ${top} "b" 0.25
    done
done

echo "SELECTION TESTING"
for selection in "b" "rs" "er" "r" #selection methods 
do
    for pop in 16 30 64 
    do
        python3 interface.py HG-3SAT-V250-C1000-7.cnf ${pop} "ri" ${selection} 0.25
    done
done

echo "MUTATION TESTING"
for prob in 0.01 0.1 0.25 0.5 #mut prob 
do
    for pop in 16 30 64 
    do
        python3 interface.py HG-3SAT-V250-C1000-7.cnf ${pop} "ri" "b" ${prob}
    done
done