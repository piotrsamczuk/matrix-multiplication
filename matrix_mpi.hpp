#pragma once

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mpi.h>
#include <random>
#include <vector>

std::vector<std::vector<double>> generateMatrix(int rows, int cols)
{
    std::random_device rd;  // seed
    std::mt19937 gen(rd()); // Mersenne Twister
    std::uniform_real_distribution<> dis(0.0, 1.0);

    std::vector<std::vector<double>> matrix(rows, std::vector<double>(cols));
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
        {
            matrix[i][j] = dis(gen);
        }
    }
    return matrix;
}

// Funkcja do konwersji macierzy 2D na 1D
std::vector<double> convertTo1D(const std::vector<std::vector<double>>& matrix)
{
    int rows = matrix.size();
    int cols = matrix[0].size();
    std::vector<double> result(rows * cols);

    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
        {
            result[i * cols + j] = matrix[i][j];
        }
    }
    return result;
}

// Funkcja do konwersji macierzy 1D na 2D
std::vector<std::vector<double>> convertTo2D(const std::vector<double>& flat, int rows, int cols)
{
    std::vector<std::vector<double>> result(rows, std::vector<double>(cols));
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
        {
            result[i][j] = flat[i * cols + j];
        }
    }
    return result;
}

// Funkcja do mnożenia części macierzy
std::vector<double> multiplyMatrixPortion(const std::vector<double>& A_portion, const std::vector<double>& B,
                                          int portion_rows, int cols, int inner_dim)
{
    std::vector<double> C_portion(portion_rows * cols, 0.0);
    for (int i = 0; i < portion_rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
        {
            for (int k = 0; k < inner_dim; ++k)
            {
                C_portion[i * cols + j] += A_portion[i * inner_dim + k] * B[k * cols + j];
            }
        }
    }
    return C_portion;
}

// Główna funkcja do rozproszonego mnożenia macierzy
std::vector<std::vector<double>> multiplyMatricesMPI(const std::vector<std::vector<double>>& A,
                                                     const std::vector<std::vector<double>>& B)
{
    int rank, num_processes;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_processes);

    int rows = A.size();
    int cols = B[0].size();
    int inner_dim = A[0].size();

    // Konwersja macierzy wejściowych do formatu 1D
    std::vector<double> flat_A = convertTo1D(A);
    std::vector<double> flat_B = convertTo1D(B);

    // Obliczenie rozmiaru porcji dla każdego procesu
    int basic_rows_per_process = rows / num_processes;
    int remainder = rows % num_processes;
    int my_portion_rows = basic_rows_per_process + (rank < remainder ? 1 : 0);

    // Przygotowanie buforów na dane
    std::vector<int> sendcounts(num_processes);
    std::vector<int> displs(num_processes);
    int current_displacement = 0;

    // Obliczenie rozmiarów i przesunięć dla każdego procesu
    for (int i = 0; i < num_processes; ++i)
    {
        int rows_for_process = basic_rows_per_process + (i < remainder ? 1 : 0);
        sendcounts[i] = rows_for_process * inner_dim;
        displs[i] = current_displacement;
        current_displacement += sendcounts[i];
    }

    // Alokacja bufora na lokalną część macierzy A
    std::vector<double> my_A_portion(my_portion_rows * inner_dim);

    // Rozdzielenie macierzy A między procesy
    MPI_Scatterv(flat_A.data(), sendcounts.data(), displs.data(), MPI_DOUBLE, my_A_portion.data(),
                 my_portion_rows * inner_dim, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Rozesłanie całej macierzy B do wszystkich procesów
    MPI_Bcast(flat_B.data(), inner_dim * cols, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Mnożenie przydzielonej części
    std::vector<double> my_C_portion = multiplyMatrixPortion(my_A_portion, flat_B, my_portion_rows, cols, inner_dim);

    // Przygotowanie buforów na wyniki
    for (int i = 0; i < num_processes; ++i)
    {
        sendcounts[i] = (basic_rows_per_process + (i < remainder ? 1 : 0)) * cols;
        displs[i] = (i > 0) ? displs[i - 1] + sendcounts[i - 1] : 0;
    }

    // Alokacja bufora na całą macierz wynikową (tylko dla procesu głównego)
    std::vector<double> flat_C;
    if (rank == 0)
    {
        flat_C.resize(rows * cols);
    }

    // Zebranie wyników od wszystkich procesów
    MPI_Gatherv(my_C_portion.data(), my_portion_rows * cols, MPI_DOUBLE, flat_C.data(), sendcounts.data(),
                displs.data(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Konwersja wyniku na format 2D (tylko dla procesu głównego)
    if (rank == 0)
    {
        return convertTo2D(flat_C, rows, cols);
    }

    // Pozostałe procesy zwracają pustą macierz
    return std::vector<std::vector<double>>();
}

// Funkcja do wykonania procedury testowej w środowisku rozproszonym
void projectProcedureMPI(const int size, const std::string& filename)
{
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Generowanie macierzy tylko na procesie głównym
    std::vector<std::vector<double>> A, B;
    if (rank == 0)
    {
        A = generateMatrix(size, size);
        B = generateMatrix(size, size);
    }

    // Synchronizacja wszystkich procesów przed rozpoczęciem
    MPI_Barrier(MPI_COMM_WORLD);
    auto start = std::chrono::high_resolution_clock::now();

    // Wykonanie mnożenia rozproszonego
    auto C = multiplyMatricesMPI(A, B);

    // Pomiar czasu tylko na procesie głównym
    if (rank == 0)
    {
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end - start;

        int num_processes;
        MPI_Comm_size(MPI_COMM_WORLD, &num_processes);

        // Przybliżone zużycie pamięci na proces
        double memory = (3 * size * size * sizeof(double)) / (1024.0 * 1024.0 * num_processes);

        std::cout << "MPI Matrix size: " << size << "x" << size << std::endl;
        std::cout << "Number of processes: " << num_processes << std::endl;
        std::cout << "MPI Execution time: " << elapsed.count() << " s" << std::endl;
        std::cout << "MPI Used memory per process: " << std::fixed << std::setprecision(2) << memory << " MB"
                  << std::endl
                  << std::endl;

        // Zapis wyników do pliku
        std::fstream file(filename, std::ios::app);
        if (file.is_open())
        {
            file << size << "," << elapsed.count() << "," << memory << "," << num_processes << std::endl;
            file.close();
        }
        else
        {
            std::cerr << "Nie można otworzyć pliku " << filename << std::endl;
        }
    }
}
