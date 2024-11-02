import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

def create_histograms(filename, output_prefix):
    # Sprawdź czy plik istnieje
    if not os.path.exists(filename):
        print(f"Plik {filename} nie istnieje!")
        return

    # Wczytaj dane z pliku CSV
    data = pd.read_csv(filename, names=['size', 'time', 'memory', 'processes'])

    # Pobierz unikalne rozmiary macierzy i liczby procesów
    sizes = sorted(data['size'].unique())
    processes = sorted(data['processes'].unique())

    # Ustawienia stylu dla wszystkich wykresów
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({'font.size': 12})

    # Dla każdego rozmiaru macierzy
    for size in sizes:
        # Filtruj dane dla danego rozmiaru
        size_data = data[data['size'] == size]

        # Jeśli to dane sekwencyjne (processes == 0) lub równoległe
        if len(processes) == 1:
            # Twórz nowy wykres
            plt.figure(figsize=(10, 6))

            # Twórz histogram czasu wykonania z logarytmicznym skalowaniem osi Y
            sns.histplot(data=size_data, x='time', bins=30, kde=True)
            plt.yscale('log')  # Dodane skalowanie logarytmiczne osi Y

            # Opcjonalnie można też dodać skalowanie logarytmiczne osi X
            if size_data['time'].max() / size_data['time'].min() > 10:
                plt.xscale('log')

            # Dodaj średnią jako pionową linię
            mean_time = size_data['time'].mean()
            plt.axvline(mean_time, color='red', linestyle='--',
                       label=f'Średnia: {mean_time:.4f}s')

            # Dodaj informacje o pamięci do tytułu
            mean_memory = size_data['memory'].mean()
            num_processes = size_data['processes'].iloc[0]

            if num_processes == 0:
                version_info = "Wersja sekwencyjna"
            else:
                version_info = f"Liczba procesów: {num_processes}"

            plt.title(f'Histogram czasu wykonania dla macierzy {size}x{size}\n'
                     f'{version_info}, Średnie zużycie pamięci: {mean_memory:.2f} MB\n'
                     f'(skala logarytmiczna)')

            plt.xlabel('Czas wykonania (s)')
            plt.ylabel('Liczba wystąpień (skala log)')
            plt.legend()

            # Zapisz wykres
            output_name = f'{output_prefix}_size_{size}'
            if num_processes > 0:
                output_name += f'_proc_{num_processes}'
            plt.savefig(f'pictures/{output_name}.png', dpi=300, bbox_inches='tight')
            plt.close()

            print(f"Utworzono histogram dla rozmiaru {size}x{size}" +
                  (f" i {num_processes} procesów" if num_processes > 0 else ""))

def main():
    # Utwórz histogramy dla wersji sekwencyjnej
    create_histograms('results/sequential_results.csv', 'sequential')

    # Utwórz histogramy dla wszystkich plików z wersji równoległej
    parallel_files = glob.glob("results/parallel_results_*proc.csv")
    for file in parallel_files:
        output_prefix = f"parallel_{os.path.basename(file).split('.')[0]}"
        create_histograms(file, output_prefix)

    print("\nAnaliza zakończona!")

if __name__ == "__main__":
    main()
