
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import sys
from matplotlib.animation import FuncAnimation

def live_plotter():
    # Set plot style
    plt.style.use('ggplot')
    
    # Create figure and axes with improved styling
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.set_facecolor('#f0f0f0')
    ax.set_facecolor('#f8f8f8')
    
    # Set title and labels with improved styling
    ax.set_title("Boid Simulation - Live Average Loss", fontsize=16, fontweight='bold')
    ax.set_xlabel("Time (seconds)", fontsize=12)
    ax.set_ylabel("Average Loss (RMSE)", fontsize=12)
    
    # Create a line with improved styling
    line, = ax.plot([], [], marker="o", linestyle="-", color="#1f77b4", linewidth=2, 
                   markersize=4, alpha=0.8)
    
    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add a horizontal line at y=0 for reference
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    
    # Initial empty data
    data = {'time': [], 'loss': []}
    
    # Maximum number of points to display (for better performance)
    max_points = 500
    
    # File paths
    data_dir = "simulation_data"
    file_path = os.path.join(data_dir, "loss_data.csv")
    flag_file = os.path.join(data_dir, "plotter_active.flag")
    
    def init():
        return line,
    
    def update(frame):
        # Check if we should continue running
        if not os.path.exists(flag_file):
            plt.close(fig)
            return line,
        
        # Check if the data file exists
        if os.path.exists(file_path):
            try:
                # Read the latest data
                df = pd.read_csv(file_path)
                if not df.empty:
                    # Update our data storage
                    data['time'] = df['time'].tolist()
                    data['loss'] = df['loss'].tolist()
                    
                    # Limit to the most recent points
                    if len(data['time']) > max_points:
                        data['time'] = data['time'][-max_points:]
                        data['loss'] = data['loss'][-max_points:]
                    
                    # Update the line data
                    line.set_data(data['time'], data['loss'])
                    
                    # Dynamically adjust y-axis limits based on data
                    if data['loss']:
                        min_y = min(0, min(data['loss'])) * 0.9
                        max_y = max(data['loss']) * 1.1
                        ax.set_ylim(min_y, max_y)
                    
                    # Adjust x-axis
                    if data['time']:
                        min_x = min(data['time'])
                        max_x = max(data['time'])
                        ax.set_xlim(min_x - 0.5, max_x + 0.5)
                    
                    # Add a rolling average line if we have enough data
                    if len(data['loss']) > 10:
                        # This creates a rolling average with a window of 10 points
                        rolling_avg = pd.Series(data['loss']).rolling(window=10).mean()
                        # If there's already an average line, update it, otherwise create a new one
                        avg_line = ax.get_lines()
                        if len(avg_line) > 1:
                            avg_line[1].set_data(data['time'][-len(rolling_avg.dropna()):], 
                                              rolling_avg.dropna())
                        else:
                            ax.plot(data['time'][-len(rolling_avg.dropna()):], 
                                  rolling_avg.dropna(), 
                                  'r--', 
                                  linewidth=1.5, 
                                  alpha=0.8, 
                                  label='10-point moving average')
                            ax.legend(loc='upper right')
            except Exception as e:
                print(f"Error reading data: {e}")
                # This can happen if the file is being written to
                pass
                
        return line,
    
    # Create animation that calls update function every 100ms
    ani = FuncAnimation(fig, update, frames=None, init_func=init, 
                      interval=100, blit=True)
    
    # Add plot title
    plt.title("Boid Simulation - Live Average Loss")
    plt.tight_layout()
    
    # Show the plot in interactive mode
    plt.show()
    
    # If the window is closed, exit cleanly
    sys.exit(0)

if __name__ == "__main__":
    live_plotter()
