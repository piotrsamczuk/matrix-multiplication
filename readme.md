### Aby uruchomić pojedyncze testy, należy:

Dla wersji sekwencyjnej:
`mpirun -np 1 --use-hwthread-cpus ./matrix-multiplication`

Dla wersji równoległej (przykład dla 4 procesów):
`mpirun -np 4 --use-hwthread-cpus ./matrix-multiplication`

### Uruchomienie zestawu testów (1, 2, 4, 8, 12 - procesów)

Stworzony skrypt uruchomić w katalogu repozytorium:
`./run_tests.sh`