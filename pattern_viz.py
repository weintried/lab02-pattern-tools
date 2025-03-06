import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_maze_patterns(file_path):
    """
    Reads maze patterns from a text file.
    
    Each pattern is separated by a blank line.
    Returns a list of 2D numpy arrays representing the patterns.
    """
    patterns = []
    current_pattern = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # If it's an empty line and we have a pattern, add it to the list
            if not line and current_pattern:
                patterns.append(np.array(current_pattern, dtype=int))
                current_pattern = []
            # If it's not an empty line, add it to the current pattern
            elif line:
                # Convert line to a list of integers
                row = [int(value) for value in line.split()]
                current_pattern.append(row)
    
    # Add the last pattern if there is one
    if current_pattern:
        patterns.append(np.array(current_pattern, dtype=int))
    
    return patterns

def solve_maze(maze):
    """
    Solve the maze using Breadth-First Search.
    Start position is top-left (0,0).
    End position is bottom-right (rows-1, cols-1).
    Returns the solution path as a list of coordinates.
    """
    maze_array = np.array(maze)
    rows, cols = maze_array.shape
    
    # Define start and end positions
    start = (0, 0)
    end = (rows-1, cols-1)
    
    # Check if start or end positions are walls
    if maze_array[start] == 1 or maze_array[end] == 1:
        return None  # No solution if start or end is a wall
    
    # Queue for BFS - store (position, path)
    queue = [(start, [start])]
    
    # Set to track visited positions
    visited = set([start])
    
    # Possible movements: right, down, left, up
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        (r, c), path = queue.pop(0)
        
        # Check if we reached the end
        if (r, c) == end:
            return path
        
        # Try all possible moves
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            # Check if the new position is valid
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze_array[nr, nc] != 1 and  # Not a wall
                (nr, nc) not in visited):  # Not visited yet
                
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    
    # If we exhaust the queue without finding a path
    return None  # No solution

def plot_maze(maze, ax=None, show_solution=True):
    """
    Plots the maze using matplotlib and shows gridlines.
    If ax is provided, plots on that axis. Otherwise creates a new figure.
    
    Color scheme:
    0: White (path)
    1: Black (wall)
    2: Yellow (start position)
    3: Red (end position)
    
    If show_solution is True, also plots the solution path from top-left to bottom-right.
    """
    maze_array = np.array(maze)
    
    # Set up the maze
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    # Create a custom colormap for the maze
    colors = ['white', 'black', 'yellow', 'red']
    cmap = ListedColormap(colors)
    
    # Display the maze with the custom colormap
    im = ax.imshow(maze_array, cmap=cmap, origin="upper", vmin=0, vmax=3)
    
    # Get the shape of the maze
    rows, cols = maze_array.shape
    
    # Set major ticks at grid cell boundaries
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    
    # Turn on grid for minor ticks
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
    
    # Remove major ticks
    ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
    
    # Add markers for start and end positions
    for i in range(rows):
        for j in range(cols):
            if maze_array[i, j] == 2:  # Sword position
                ax.text(j, i, 'S', ha='center', va='center', color='black', fontweight='bold')
            elif maze_array[i, j] == 3:  # Monster position
                ax.text(j, i, 'M', ha='center', va='center', color='white', fontweight='bold')
    
    # Add solution path if requested
    if show_solution:
        solution = solve_maze(maze_array)
        if solution:
            # Extract x and y coordinates for the path
            y_coords, x_coords = zip(*solution)
            
            # Plot the path as a line
            ax.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.7)
            
            # Mark the start and end points
            ax.plot(x_coords[0], y_coords[0], 'go', markersize=8)  # Start
            ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=8)  # End
            
            # Add a small message showing if there's a solution
            ax.text(0.5, 0.01, "Solution Found", transform=ax.transAxes, 
                    ha='center', va='bottom', color='green', 
                    bbox=dict(facecolor='white', alpha=0.7))
        else:
            # Add a message if no solution exists
            ax.text(0.5, 0.01, "No Solution Exists", transform=ax.transAxes, 
                    ha='center', va='bottom', color='red',
                    bbox=dict(facecolor='white', alpha=0.7))
    
    # Highlight odd, odd cells in purple
    for i in range(1, rows, 2):
        for j in range(1, cols, 2):
            ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color='magenta', alpha=0.3))
    
    return ax

class MazeVisualizerApp:
    def __init__(self, root, patterns):
        self.root = root
        self.patterns = patterns
        self.current_pattern_idx = 0
        
        # Configure the root window
        self.root.title("Maze Pattern Visualizer")
        self.root.geometry("800x800")
        
        # Create frame for controls
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(fill=tk.X)
        
        # Create pattern selector
        self.pattern_selector_label = ttk.Label(self.control_frame, text="Select Pattern:")
        self.pattern_selector_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.pattern_var = tk.StringVar()
        self.pattern_selector = ttk.Combobox(
            self.control_frame, 
            textvariable=self.pattern_var,
            values=[f"Pattern {i+1}" for i in range(len(patterns))],
            width=15
        )
        self.pattern_selector.current(0)
        self.pattern_selector.pack(side=tk.LEFT)
        self.pattern_selector.bind("<<ComboboxSelected>>", self.on_pattern_selected)
        
        # Create index display
        self.index_label = ttk.Label(
            self.control_frame, 
            text=f"Pattern {self.current_pattern_idx + 1}/{len(patterns)}"
        )
        self.index_label.pack(side=tk.LEFT, padx=20)
        
        # Create buttons for navigation
        self.prev_button = ttk.Button(self.control_frame, text="Previous", command=self.prev_pattern)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        
        self.next_button = ttk.Button(self.control_frame, text="Next", command=self.next_pattern)
        self.next_button.pack(side=tk.LEFT)
        
        # Create legend frame
        self.legend_frame = ttk.Frame(root, padding="5")
        self.legend_frame.pack(fill=tk.X)
        
        # Create legend items
        legend_label = ttk.Label(self.legend_frame, text="Legend:")
        legend_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Path legend
        path_label = ttk.Label(self.legend_frame, text="Path (0):", anchor="e")
        path_label.pack(side=tk.LEFT, padx=(0, 5))
        path_canvas = tk.Canvas(self.legend_frame, width=20, height=20, bg="white", highlightbackground="gray", highlightthickness=1)
        path_canvas.pack(side=tk.LEFT, padx=(0, 15))
        
        # Wall legend
        wall_label = ttk.Label(self.legend_frame, text="Wall (1):", anchor="e")
        wall_label.pack(side=tk.LEFT, padx=(0, 5))
        wall_canvas = tk.Canvas(self.legend_frame, width=20, height=20, bg="black", highlightbackground="gray", highlightthickness=1)
        wall_canvas.pack(side=tk.LEFT, padx=(0, 15))
        
        # Sword legend
        sword_label = ttk.Label(self.legend_frame, text="Sword (2):", anchor="e")
        sword_label.pack(side=tk.LEFT, padx=(0, 5))
        sword_canvas = tk.Canvas(self.legend_frame, width=20, height=20, bg="yellow", highlightbackground="gray", highlightthickness=1)
        sword_canvas.create_text(10, 10, text="S", fill="black", font=("TkDefaultFont", 10, "bold"))
        sword_canvas.pack(side=tk.LEFT, padx=(0, 15))
        
        # Monster legend
        monster_label = ttk.Label(self.legend_frame, text="Monster (3):", anchor="e")
        monster_label.pack(side=tk.LEFT, padx=(0, 5))
        monster_canvas = tk.Canvas(self.legend_frame, width=20, height=20, bg="red", highlightbackground="gray", highlightthickness=1)
        monster_canvas.create_text(10, 10, text="M", fill="white", font=("TkDefaultFont", 10, "bold"))
        monster_canvas.pack(side=tk.LEFT)
        
        # Create a figure for the plot
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        
        # Create a canvas to display the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display the first pattern
        self.update_plot()
        self.update_button_states()
    
    def update_plot(self):
        self.ax.clear()
        plot_maze(self.patterns[self.current_pattern_idx], self.ax)
        self.ax.set_title(f"Pattern {self.current_pattern_idx + 1}")
        self.pattern_selector.current(self.current_pattern_idx)
        self.index_label.config(text=f"Pattern {self.current_pattern_idx + 1}/{len(self.patterns)}")
        self.canvas.draw()
    
    def update_button_states(self):
        # Enable/disable navigation buttons based on current index
        self.prev_button.config(state=tk.NORMAL if self.current_pattern_idx > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_pattern_idx < len(self.patterns) - 1 else tk.DISABLED)
    
    def on_pattern_selected(self, event):
        selected_idx = self.pattern_selector.current()
        if 0 <= selected_idx < len(self.patterns):
            self.current_pattern_idx = selected_idx
            self.update_plot()
            self.update_button_states()
    
    def next_pattern(self):
        if self.current_pattern_idx < len(self.patterns) - 1:
            self.current_pattern_idx += 1
            self.update_plot()
            self.update_button_states()
    
    def prev_pattern(self):
        if self.current_pattern_idx > 0:
            self.current_pattern_idx -= 1
            self.update_plot()
            self.update_button_states()

def main():
    try:
        # Read the maze patterns from the file
        file_path = "input.txt"  # Update this path if necessary
        patterns = read_maze_patterns(file_path)
        
        if not patterns:
            print("No patterns found in the input file.")
            return
        
        # Create the Tkinter application
        root = tk.Tk()
        app = MazeVisualizerApp(root, patterns)
        root.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()