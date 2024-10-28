import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_histograms(filename, output_prefix):
    # Sprawdź czy plik istnieje
    if not os.path.exists(filename):
        print(f"Plik {filename} nie istnieje!")
        return
    
    # Wczytaj dane z pliku CSV
    # Sprawdź liczbę kolumn w pliku aby określić czy zawiera dane o liczbie procesów
    with open(filename) as f:
        first_line = f.readline()
        num_columns = len(first_line.strip().split(','))
    
    if num_columns == 4:
        # Plik zawiera dane z wersji rozproszonej
        names = ['size', 'time', 'memory', 'processes']
    else:
        # Plik zawiera dane z wersji sekwencyjnej
        names = ['size', 'time', 'memory']
    
    data = pd.read_csv(filename, names=names)
    
    # Pobierz unikalne rozmiary macierzy
    sizes = sorted(data['size'].unique())
    
    # Ustawienia stylu dla wszystkich wykresów
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({'font.size': 12})
    
    # Dla każdego rozmiaru macierzy
    for size in sizes:
        # Filtruj dane dla danego rozmiaru
        size_data = data[data['size'] == size]
        
        # Twórz nowy wykres
        plt.figure(figsize=(10, 6))
        
        # Twórz histogram czasu wykonania
        sns.histplot(data=size_data, x='time', bins=30, kde=True)
        
        # Dodaj średnią jako pionową linię
        mean_time = size_data['time'].mean()
        plt.axvline(mean_time, color='red', linestyle='--', label=f'Średnia: {mean_time:.4f}s')
        
        # Dodaj informacje o pamięci do tytułu
        mean_memory = size_data['memory'].mean()
        
        # Ustawienia wykresu
        if 'processes' in size_data.columns:
            num_processes = size_data['processes'].iloc[0]
            plt.title(f'Histogram czasu wykonania dla macierzy {size}x{size}\n'
                     f'Liczba procesów: {num_processes}, Średnie zużycie pamięci: {mean_memory:.2f} MB')
        else:
            plt.title(f'Histogram czasu wykonania dla macierzy {size}x{size}\n'
                     f'Wersja sekwencyjna, Średnie zużycie pamięci: {mean_memory:.2f} MB')
        
        plt.xlabel('Czas wykonania (s)')
        plt.ylabel('Liczba wystąpień')
        plt.legend()
        
        # Zapisz wykres
        plt.savefig(f'{output_prefix}_size_{size}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Utworzono histogram dla rozmiaru {size}x{size}")

def main():
    # Utwórz histogramy dla obu wersji jeśli pliki istnieją
    create_histograms('histogram.csv', 'sequential')
    create_histograms('histogram_distributed.csv', 'distributed')
    
    print("\nAnaliza zakończona!")

if __name__ == "__main__":
    main()