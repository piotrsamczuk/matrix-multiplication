import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytaj dane z pliku CSV
data = pd.read_csv("log.csv", names=['size', 'time', 'memory'])

# Ustawienia stylów
sns.set_theme(style="darkgrid")

# Tworzenie wykresu liniowego dla czasu wykonania i zużycia pamięci
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Wykres czasu wykonania
sns.lineplot(x='size', y='time', data=data, ax=ax1, marker='o')
ax1.set_title('Czas wykonania w zależności od rozmiaru macierzy')
ax1.set_xlabel('Rozmiar macierzy')
ax1.set_ylabel('Czas wykonania (s)')

# Wykres zużycia pamięci
sns.lineplot(x='size', y='memory', data=data, ax=ax2, marker='o')
ax2.set_title('Zużycie pamięci w zależności od rozmiaru macierzy')
ax2.set_xlabel('Rozmiar macierzy')
ax2.set_ylabel('Zużycie pamięci (MB)')

# Dostosowanie układu
plt.tight_layout()

# Zapisanie wykresu liniowego
plt.savefig('matrix_multiplication_results.png', dpi=300)

# Dodatkowa analiza - korelacja
correlation = data['size'].corr(data['time'])
print(f"Korelacja między rozmiarem macierzy a czasem wykonania: {correlation:.2f}")

# Analiza wzrostu złożoności
data['time_ratio'] = data['time'] / data['time'].shift(1)
data['size_ratio'] = data['size'] / data['size'].shift(1)
data['complexity_growth'] = data['time_ratio'] / (data['size_ratio'] ** 3)

print("\nWzrost złożoności czasowej:")
print(data[['size', 'time', 'complexity_growth']].to_string(index=False))

# Wykres log-log
plt.figure(figsize=(8, 6))
sns.lineplot(x='size', y='time', data=data, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.title('Wykres log-log: Czas wykonania vs Rozmiar macierzy')
plt.xlabel('Rozmiar macierzy (log scale)')
plt.ylabel('Czas wykonania (s) (log scale)')
plt.savefig('log_log_plot.png', dpi=300)
