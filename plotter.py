import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
from tqdm import tqdm

print("Starting data loading and analysis...")

# Wczytaj dane sekwencyjne
print("\nLoading sequential data...")
data_seq = pd.read_csv("results/sequential_results.csv", names=['size', 'time', 'memory', 'processes'])

# Wczytaj wszystkie pliki z danymi równoległymi
print("\nLoading parallel data...")
parallel_files = glob.glob("results/parallel_results_*proc.csv")
data_parallel = []
for file in tqdm(parallel_files, desc="Loading parallel files"):
    df = pd.read_csv(file, names=['size', 'time', 'memory', 'processes'])
    data_parallel.append(df)

# Połącz wszystkie dane równoległe
print("\nCombining parallel data...")
data_mpi = pd.concat(data_parallel)

# Wyświetl przykładowe dane przed zapisem
print("\nPrzykładowe dane sekwencyjne:")
print(data_seq.head())
print("\nRozmiar danych sekwencyjnych:", data_seq.memory_usage().sum() / 1024 / 1024, "MB")

print("\nPrzykładowe dane równoległe:")
print(data_mpi.head())
print("\nRozmiar danych równoległych:", data_mpi.memory_usage().sum() / 1024 / 1024, "MB")

# [... kod generujący wykresy pozostaje bez zmian ...]

print("\nSaving optimized analysis results...")
# Zapisz tylko najważniejsze metryki do CSV
for num_proc in tqdm(sorted(data_mpi['processes'].unique()), desc="Saving analysis results"):
    data_proc = data_mpi[data_mpi['processes'] == num_proc]

    # Tworzenie zoptymalizowanego DataFrame z tylko potrzebnymi kolumnami

    ### ZMIENIC LOSOWE LICZBY W DATAFRAME NA SREDNIA/MINIMUM/MEDIANE 

    analysis_df = pd.DataFrame({
        'matrix_size': data_proc['size'],
        'sequential_time': data_seq['time'],
        'parallel_time': data_proc['time'],
        'speedup': data_seq['time'] / data_proc['time'],
        'efficiency': (data_seq['time'] / data_proc['time']) / num_proc,
        'num_processes': data_proc['processes']
    })

    # Wyświetl rozmiar pliku przed zapisem
    print(f"\nRozmiar danych dla {num_proc} procesów:",
          analysis_df.memory_usage().sum() / 1024 / 1024, "MB")

    # Zapisz z kompresją
    analysis_df.to_csv(
        f'results/analysis_results_{num_proc}proc.csv',
        index=False,
        float_format='%.4f'  # Ogranicz precyzję liczb zmiennoprzecinkowych
    )

print("\nAll operations completed successfully!")
