import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import os
import glob
import numpy as np

def create_interactive_histograms(filename, output_prefix):
    # Check if file exists
    if not os.path.exists(filename):
        print(f"File {filename} does not exist!")
        return

    # Read CSV data
    data = pd.read_csv(filename, names=['size', 'time', 'memory', 'processes'])

    # Get unique matrix sizes and process counts
    sizes = sorted(data['size'].unique())
    processes = sorted(data['processes'].unique())

    # Ensure pictures directory exists
    os.makedirs('pictures', exist_ok=True)

    # For each matrix size
    for size in sizes:
        # Filter data for specific size
        size_data = data[data['size'] == size]

        # Convert time to milliseconds
        time_ms = size_data['time'] * 1000  # Convert to milliseconds

        # Determine bin count
        num_bins = min(30, int(np.sqrt(len(time_ms))))

        # Calculate histogram data
        hist, bin_edges = np.histogram(time_ms, bins=num_bins)
        
        # Prepare bin labels (centers of bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Create interactive Plotly histogram
        fig = go.Figure()

        # Add histogram trace
        fig.add_trace(go.Bar(
            x=bin_centers,
            y=hist,
            width=[bin_edges[1] - bin_edges[0]] * len(hist),
            text=[f'Count: {count}<br>Range: {bin_edges[i]:.2f}-{bin_edges[i+1]:.2f} ms' for i, count in enumerate(hist)],
            hoverinfo='text',
            marker_color='rgba(58, 71, 80, 0.6)',
            marker_line_color='rgba(58, 71, 80, 1.0)',
            marker_line_width=1.5
        ))

        # Customize layout
        num_processes = size_data['processes'].iloc[0]
        version_info = "Sequential" if num_processes == 0 else f"Parallel ({num_processes} processes)"
        
        fig.update_layout(
            title=f'Execution Time Distribution for {size}x{size} Matrix<br>{version_info}',
            xaxis_title='Execution Time (ms)',
            yaxis_title='Frequency',
            yaxis_type='log',
            yaxis_range=[0, None],  # This ensures y-axis starts at actual zero
            hovermode='closest'
        )

        # Ensure y-axis starts at 1
        fig.update_yaxes(
            rangemode='nonnegative',  # Ensures non-negative values
            nticks=10  # Adjust number of ticks as needed
        )

        # Add annotations with statistical information
        stats_text = (
            f"Total Samples: {len(time_ms)}<br>"
            f"Mean: {time_ms.mean():.2f} ms<br>"
            f"Median: {time_ms.median():.2f} ms<br>"
            f"Std Dev: {time_ms.std():.2f} ms<br>"
            f"Min: {time_ms.min():.2f} ms<br>"
            f"Max: {time_ms.max():.2f} ms"
        )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.95,
            y=0.95,
            text=stats_text,
            showarrow=False,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='lightgray'
        )

        # Save as interactive HTML
        output_name = f'{output_prefix}_size_{size}'
        if num_processes > 0:
            output_name += f'_proc_{num_processes}'
        
        html_filename = f'pictures/{output_name}_interactive.html'
        pio.write_html(fig, file=html_filename, auto_open=False)

        print(f"Created interactive histogram for size {size}x{size}" +
              (f" with {num_processes} processes" if num_processes > 0 else ""))

def main():
    # Create histograms for sequential version
    create_interactive_histograms('results/sequential_results.csv', 'sequential')

    # Create histograms for all parallel files
    parallel_files = glob.glob("results/parallel_results_*proc.csv")
    for file in parallel_files:
        output_prefix = f"parallel_{os.path.basename(file).split('.')[0]}"
        create_interactive_histograms(file, output_prefix)

    print("\nAnalysis completed!")

if __name__ == "__main__":
    main()