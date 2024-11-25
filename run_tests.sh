#!/bin/bash

for np in 1 2 4 6 8 12
do
    echo "Uruchamianie dla $np procesów:"
    mpirun -np $np ./build/matrix-multiplication
    echo "---------------------------------"
done
