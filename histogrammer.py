import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np

def create_histograms(filename, output_prefix):
    # Check if file exists
    if not os.path.exists(filename):
        print(f"File {filename} does not exist!")
        return

    # Read CSV data
    data = pd.read_csv(filename, names=['size', 'time', 'memory', 'processes'])

    # Get unique matrix sizes and process counts
    sizes = sorted(data['size'].unique())
    processes = sorted(data['processes'].unique())

    # Style settings for all plots
    plt.style.use('default')  # Prosty, domyślny styl
    plt.rcParams.update({
        'font.size': 12,
        'grid.linestyle': ':',
        'grid.color': 'gray',
        'grid.alpha': 0.7
    })

    # For each matrix size
    for size in sizes:
        # Filter data for specific size
        size_data = data[data['size'] == size]

        # Create new figure
        plt.figure(figsize=(10, 6))

        # Convert time to milliseconds
        time_ms = size_data['time'] * 1000  # Convert to milliseconds
        
         # Create histogram with logarithmic y-scale 
        plt.hist(time_ms, bins=30, edgecolor='black', alpha=0.7)
        plt.yscale('log')  # Logarithmic y-axis
        
        # Set y-axis to start from 0
        plt.ylim(bottom=0)
        
        # Add gridlines
        plt.grid(True, which='major', linestyle='-', linewidth=0.8, color='black', alpha=0.8)
        plt.grid(True, which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.6)
        
        # Scientific notation for x-axis
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

        num_processes = size_data['processes'].iloc[0]
        version_info = "Sequential" if num_processes == 0 else f"Parallel ({num_processes} processes)"

        plt.title(f'Execution Time Distribution for {size}x{size} Matrix\n'
                  f'{version_info}')

        plt.xlabel('Execution Time (ms)')
        plt.ylabel('Frequency')

        # Save plot
        output_name = f'{output_prefix}_size_{size}'
        if num_processes > 0:
            output_name += f'_proc_{num_processes}'
        plt.savefig(f'pictures/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Created histogram for size {size}x{size}" +
              (f" with {num_processes} processes" if num_processes > 0 else ""))

def main():
    # Create histograms for sequential version
    create_histograms('results/sequential_results.csv', 'sequential')

    # Create histograms for all parallel files
    parallel_files = glob.glob("results/parallel_results_*proc.csv")
    for file in parallel_files:
        output_prefix = f"parallel_{os.path.basename(file).split('.')[0]}"
        create_histograms(file, output_prefix)

    print("\nAnalysis completed!")

if __name__ == "__main__":
    main()