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

print("\nSaving optimized analysis results...")
# Save only key metrics to CSV
for num_proc in tqdm(sorted(data_mpi['processes'].unique()), desc="Saving analysis results"):
    data_proc = data_mpi[data_mpi['processes'] == num_proc]

    # Compute median values for each size
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
            'sequential_time': median_seq_time,
            'parallel_time': median_parallel_time,
            'speedup': speedup,
            'efficiency': efficiency,
            'num_processes': num_proc
        })

    analysis_df = pd.DataFrame(analysis_data)

    # Save with compression
    analysis_df.to_csv(
        f'results/analysis_results_{num_proc}proc.csv',
        index=False,
        float_format='%.4f'
    )

    # Create speedup and efficiency plots
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(analysis_df['matrix_size'], analysis_df['speedup'], marker='o')
    plt.title(f'Speedup ({num_proc} Processes)')
    plt.xlabel('Matrix Size')
    plt.ylabel('Speedup')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(analysis_df['matrix_size'], analysis_df['efficiency'], marker='o')
    plt.title(f'Efficiency ({num_proc} Processes)')
    plt.xlabel('Matrix Size')
    plt.ylabel('Efficiency')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f'pictures/speedup_efficiency_{num_proc}proc.png')
    plt.close()

print("\nAll operations completed successfully!")