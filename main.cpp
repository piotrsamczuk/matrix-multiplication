#include "matrix_mpi.hpp"
#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>

std::vector<std::vector<double>> multiplyMatrices(const std::vector<std::vector<double>>& A,
                                                  const std::vector<std::vector<double>>& B)
{
    int rowsA = A.size();
    int colsA = A[0].size();
    int colsB = B[0].size();

    std::vector<std::vector<double>> C(rowsA, std::vector<double>(colsB, 0.0));

    for (int i = 0; i < rowsA; ++i)
    {
        for (int j = 0; j < colsB; ++j)
        {
            for (int k = 0; k < colsA; ++k)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return C;
}

void saveResultsToCSV(const std::string& filename, int size, double time, double memory)
{
    std::fstream file(filename, std::ios::app);
    if (file.is_open())
    {
        file << size << "," << time << "," << memory << std::endl;
        file.close();
    }
    else
    {
        std::cerr << "Nie można otworzyć pliku " << filename << std::endl;
    }
}

void projectProcedure(const int size, const std::string& filename)
{
    const auto A = generateMatrix(size, size);
    const auto B = generateMatrix(size, size);

    const auto start = std::chrono::high_resolution_clock::now();
    const auto C = multiplyMatrices(A, B);
    const auto end = std::chrono::high_resolution_clock::now();

    const std::chrono::duration<double> elapsed = end - start;

    // Przybliżone zużycie pamięci [B -> MB], może użyć Valgrind?
    // 3 * size * size, bo mamy 3 macierze dwuwymiarowe: A, B, C
    const double memory = (3 * size * size * sizeof(double)) / (1024.0 * 1024.0);

    std::cout << "Matrix size: " << size << "x" << size << std::endl;
    std::cout << "Execution time: " << elapsed.count() << " s" << std::endl;
    std::cout << "Used memory: " << std::fixed << std::setprecision(2) << memory << " MB" << std::endl << std::endl;

    saveResultsToCSV(filename, size, elapsed.count(), memory);
}

int main()
{
    // // Inicjalizacja MPI
    // MPI_Init(&argc, &argv);
    // int rank;
    // MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    const auto cardinality = 500;
    const std::vector<int> sizes = {100, 250, 500};

    // Kod dla wersji sekwencyjnej (wykonywany tylko przez proces główny)
    // if(rank == 0)
    if (0 == 0)
    {
        for (const int& size : sizes)
        {
            for (int i = 0; i < cardinality; i++)
            {
                projectProcedure(size, "histogram.csv");
            }
        }

        for (int size = 10; size < cardinality; size++)
        {
            projectProcedure(size, "log.csv");
        }
    }

    // // Kod dla wersji rozproszonej (wykonywany przez wszystkie procesy)
    // MPI_Barrier(MPI_COMM_WORLD); // Synchronizacja przed rozpoczęciem testów MPI

    // for (const int& size : sizes)
    // {
    //     for (int i = 0; i < cardinality; i++)
    //     {
    //         projectProcedureMPI(size, "histogram_distributed.csv");
    //     }
    // }

    // for (int size = 10; size < cardinality; size++)
    // {
    //     projectProcedureMPI(size, "log_distributed.csv");
    // }

    // MPI_Finalize();
    return 0;
}
