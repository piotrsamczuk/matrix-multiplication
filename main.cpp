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

void saveResultsToCSV(const std::string& filename, int size, double time, double memory, int num_processes = 0)
{
    std::fstream file(filename, std::ios::app);
    if (file.is_open())
    {
        file << size << "," << time << "," << memory << "," << num_processes << std::endl;
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
    const double memory = (3 * size * size * sizeof(double)) / (1024.0 * 1024.0);

    std::cout << "Sequential - Matrix size: " << size << "x" << size << std::endl;
    std::cout << "Execution time: " << elapsed.count() << " s" << std::endl;
    std::cout << "Used memory: " << std::fixed << std::setprecision(2) << memory << " MB" << std::endl << std::endl;

    saveResultsToCSV(filename, size, elapsed.count(), memory, 0); // 0 oznacza wersję sekwencyjną
}

int main(int argc, char* argv[])
{
    MPI_Init(&argc, &argv);
    int rank, num_processes;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_processes);

    // Definicja parametrów eksperymentu
    const std::vector<int> matrix_sizes = {20, 50, 100, 200, 500, 700};
    const int repetitions = 1000;

    // Wersja sekwencyjna (tylko dla procesu głównego gdy num_processes == 1)
    if (rank == 0 && num_processes == 1)
    {
        std::cout << "Running sequential tests..." << std::endl;
        for (const int& size : matrix_sizes)
        {
            for (int i = 0; i < repetitions; i++)
            {
                projectProcedure(size, "results/sequential_results.csv");
            }
        }
    }

    // Wersja równoległa
    if (num_processes > 1)
    {
        MPI_Barrier(MPI_COMM_WORLD);
        if (rank == 0)
        {
            std::cout << "Running parallel tests with " << num_processes << " processes..." << std::endl;
        }

        for (const int& size : matrix_sizes)
        {
            for (int i = 0; i < repetitions; i++)
            {
                std::string filename = "results/parallel_results_" + std::to_string(num_processes) + "proc.csv";
                projectProcedureMPI(size, filename);
            }
        }
    }

    MPI_Finalize();
    return 0;
}
