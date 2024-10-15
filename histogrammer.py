import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")

# Wczytaj dane z pliku CSV
data = pd.read_csv('results.csv', names=['size', 'time', 'memory'])

# Tworzenie histogramów dla różnych rozmiarów macierzy
sizes = data['size'].unique()

# Pętla przez każdy rozmiar macierzy, aby wygenerować osobny histogram czasu wykonania
for size in sizes:
    plt.figure(figsize=(8, 6))
    size_data = data[data['size'] == size]  # Filtruj dane dla danego rozmiaru macierzy
    
    # Tworzenie histogramu dla czasu wykonania
    sns.histplot(size_data['time'], bins=20, kde=False)
    
    # Ustawienia wykresu
    plt.title(f'Histogram czasu wykonania dla macierzy {size}x{size}')
    plt.xlabel('Czas wykonania (s)')
    plt.ylabel('Częstotliwość')
    
    # Zapisanie histogramu
    plt.savefig(f'histogram_size_{size}.png', dpi=300)
    plt.show()

