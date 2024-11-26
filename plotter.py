import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
import glob
from tqdm import tqdm
import matplotlib.cm as cm

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

# Unique processes for color mapping
unique_processes = sorted(data_mpi['processes'].unique())
colors = [f'rgb({int(r*255)},{int(g*255)},{int(b*255)})' for r,g,b,_ in cm.rainbow(np.linspace(0, 1, len(unique_processes)))]

# Function to create performance traces
def create_performance_traces(data_seq, data_mpi, metric, log_scale=False):
    traces = []
    for i, num_proc in enumerate(unique_processes):
        # Filter data for specific process count
        data_proc = data_mpi[data_mpi['processes'] == num_proc]
        
        # Compute analysis data
        analysis_data = []
        for size in sorted(data_seq['size'].unique()):
            seq_data = data_seq[data_seq['size'] == size]
            parallel_data = data_proc[data_proc['size'] == size]
            
            if metric == 'speedup':
                median_seq_time = np.median(seq_data['time'])
                median_parallel_time = np.median(parallel_data['time'])
                value = median_seq_time / median_parallel_time
                y_label = 'Speedup'
            elif metric == 'efficiency':
                median_seq_time = np.median(seq_data['time'])
                median_parallel_time = np.median(parallel_data['time'])
                speedup = median_seq_time / median_parallel_time
                value = (speedup / num_proc) * 100
                y_label = 'Efficiency [%]'
            elif metric == 'memory':
                value = np.median(parallel_data['memory'])
                y_label = 'Memory Usage [MB]'
            elif metric == 'time':
                value = np.median(parallel_data['time'])
                y_label = 'Execution Time [s]'
            
            analysis_data.append({
                'matrix_size': size,
                'value': value
            })
        
        analysis_df = pd.DataFrame(analysis_data)
        
        trace = go.Scatter(
            x=analysis_df['matrix_size'],
            y=analysis_df['value'],
            mode='lines+markers',
            name=f'{num_proc} Processes',
            line=dict(color=colors[i]),
            hovertemplate='Matrix Size: %{x}<br>Value: %{y:.4f}<extra></extra>'
        )
        traces.append(trace)
    
    return traces, y_label

# Comprehensive Performance Comparison
def create_comprehensive_plot():
    # Speedup plot
    speedup_traces, speedup_label = create_performance_traces(data_seq, data_mpi, 'speedup')
    
    # Efficiency plot
    efficiency_traces, efficiency_label = create_performance_traces(data_seq, data_mpi, 'efficiency')
    
    # Create subplot figure
    fig = go.Figure()
    
    # Add speedup traces
    for trace in speedup_traces:
        fig.add_trace(trace)
    
    # Update layout for first subplot (Speedup)
    fig.update_layout(
        title='Speedup Comparison Across Different Process Counts',
        xaxis_title='Matrix Size [n]',
        yaxis_title=speedup_label,
        height=600,
        width=1000,
        hovermode='closest'
    )
    
    # Save speedup plot
    pio.write_html(fig, file='pictures/speedup_comparison.html')
    
    # Create efficiency plot
    fig = go.Figure()
    
    # Add efficiency traces
    for trace in efficiency_traces:
        fig.add_trace(trace)
    
    # Update layout for second subplot (Efficiency)
    fig.update_layout(
        title='Efficiency Comparison Across Different Process Counts',
        xaxis_title='Matrix Size [n]',
        yaxis_title=efficiency_label,
        height=600,
        width=1000,
        hovermode='closest'
    )
    
    # Save efficiency plot
    pio.write_html(fig, file='pictures/efficiency_comparison.html')

# Memory Usage Comparison
def create_memory_plot():
    # Memory usage traces
    memory_traces, memory_label = create_performance_traces(data_seq, data_mpi, 'memory')
    
    # Create figure
    fig = go.Figure()
    
    # Add memory traces
    for trace in memory_traces:
        fig.add_trace(trace)
    
    # Update layout
    fig.update_layout(
        title='Memory Usage Across Matrix Sizes',
        xaxis_title='Matrix Size [n]',
        yaxis_title=memory_label,
        height=600,
        width=1000,
        hovermode='closest'
    )
    
    # Save memory plot
    pio.write_html(fig, file='pictures/memory_usage_comparison.html')

# Execution Time Comparison (Log-Log Scale)
def create_time_plot():
    # Time traces 
    time_traces, time_label = create_performance_traces(data_seq, data_mpi, 'time')
    
    # Create figure
    fig = go.Figure()
    
    # Add time traces
    for trace in time_traces:
        fig.add_trace(trace)
    
    # Update layout with scientific notation
    fig.update_layout(
        title='Execution Time Comparison',
        xaxis_title='Matrix Size [n]',
        yaxis_title='Execution Time [ms]',  # Changed to milliseconds
        height=600,
        width=1000,
        hovermode='closest'
    )
    
    # Modify the traces to convert seconds to milliseconds
    for trace in fig.data:
        trace.y = [y * 1000 for y in trace.y]
    
    # Set y-axis to scientific notation for milliseconds
    fig.update_yaxes(
        tickformat='.2e',  # Scientific notation with 2 decimal places
        exponentformat='power'  # Show exponent as power of 10
    )
    
    # Save time plot
    pio.write_html(fig, file='pictures/execution_time_comparison.html')

# Create all plots
create_comprehensive_plot()
create_memory_plot()
create_time_plot()

print("\nInteractive performance comparison plots created successfully!")