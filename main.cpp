#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
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

int main()
{
    const std::vector<int> sizes = {100, 500, 1000, 2000}; // Rozmiary macierzy do testów

    for (const int& size : sizes)
    {
        const auto A = generateMatrix(size, size);
        const auto B = generateMatrix(size, size);

        const auto start = std::chrono::high_resolution_clock::now();
        const auto C = multiplyMatrices(A, B);
        const auto end = std::chrono::high_resolution_clock::now();

        const std::chrono::duration<double> elapsed = end - start;

        // Przybliżone zużycie pamięci (w MB)
        const double memory = (3 * size * size * sizeof(double)) / (1024.0 * 1024.0);

        std::cout << "Matrix size: " << size << "x" << size << std::endl;
        std::cout << "Execution time: " << elapsed.count() << " s" << std::endl;
        std::cout << "Used memory: " << std::fixed << std::setprecision(2) << memory << " MB" << std::endl << std::endl;

        saveResultsToCSV("results.csv", size, elapsed.count(), memory);
    }

    return 0;
}