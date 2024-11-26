#!/bin/bash

for np in 1 2 4 8 12
do
    echo "Uruchamianie dla $np procesów:"
    mpirun -np $np --use-hwthread-cpus ./build/matrix-multiplication
    echo "---------------------------------"
done
