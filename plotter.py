import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from tqdm import tqdm

print("Starting data loading and analysis...")

# Load sequential data
print("\nLoading sequential data...")
data_seq = pd.read_csv("results/sequential_results.csv", names=['size', 'time', 'memory', 'processes'])

# Load all parallel data files
print("\nLoading parallel data...")
parallel_files = glob.glob("results/parallel_results_*proc.csv")
data_parallel = []
for file in tqdm(parallel_files, desc="Loading parallel files"):
    df = pd.read_csv(file, names=['size', 'time', 'memory', 'processes'])
    data_parallel.append(df)

# Combine parallel data
print("\nCombining parallel data...")
data_mpi = pd.concat(data_parallel)

# Comprehensive analysis and plotting
print("\nPerforming comprehensive analysis...")
unique_processes = sorted(data_mpi['processes'].unique())

# Prepare figure for comprehensive comparison
plt.figure(figsize=(15, 10))

# Speedup subplot
plt.subplot(2, 1, 1)
plt.title('Speedup Comparison Across Different Process Counts', fontsize=14)
plt.xlabel('Matrix Size', fontsize=12)
plt.ylabel('Speedup', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Efficiency subplot
plt.subplot(2, 1, 2)
plt.title('Efficiency Comparison Across Different Process Counts', fontsize=14)
plt.xlabel('Matrix Size', fontsize=12)
plt.ylabel('Efficiency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Color palette for different process counts
colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_processes)))

for num_proc, color in zip(unique_processes, colors):
    # Filter data for specific process count
    data_proc = data_mpi[data_mpi['processes'] == num_proc]
    
    # Compute analysis data
    analysis_data = []
    for size in sorted(data_seq['size'].unique()):
        seq_times = data_seq[data_seq['size'] == size]['time']
        parallel_times = data_proc[data_proc['size'] == size]['time']
        
        median_seq_time = np.median(seq_times)
        median_parallel_time = np.median(parallel_times)
        
        speedup = median_seq_time / median_parallel_time
        efficiency = speedup / num_proc
        
        analysis_data.append({
            'matrix_size': size,
            'speedup': speedup,
            'efficiency': efficiency
        })

    analysis_df = pd.DataFrame(analysis_data)

    # Plot speedup
    plt.subplot(2, 1, 1)
    plt.plot(analysis_df['matrix_size'], analysis_df['speedup'], 
             marker='o', label=f'{num_proc} Processes', color=color)

    # Plot efficiency
    plt.subplot(2, 1, 2)
    plt.plot(analysis_df['matrix_size'], analysis_df['efficiency'], 
             marker='o', label=f'{num_proc} Processes', color=color)

# Add legends
plt.subplot(2, 1, 1)
plt.legend(title='Process Counts', loc='best')

plt.subplot(2, 1, 2)
plt.legend(title='Process Counts', loc='best')

# Adjust layout and save
plt.tight_layout()
plt.savefig('pictures/comprehensive_speedup_efficiency_comparison.png', dpi=300)
plt.close()

print("\nComprehensive comparison plot created successfully!")