import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#######################
# File Reading & Maze Solving Functions
#######################

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
            # Blank line indicates end of a pattern
            if not line and current_pattern:
                patterns.append(np.array(current_pattern, dtype=int))
                current_pattern = []
            elif line:
                # Each row: cells separated by space
                row = [int(value) for value in line.split()]
                current_pattern.append(row)
    if current_pattern:
        patterns.append(np.array(current_pattern, dtype=int))
    return patterns

def solve_maze(maze):
    """
    Solve the maze using BFS.
    Start: top-left (0,0); End: bottom-right.
    A cell is passable if its value is not 1 (wall).
    Returns the solution path as a list of (row, col) coordinates, or None if no solution.
    """
    maze_array = np.array(maze)
    rows, cols = maze_array.shape
    start = (0, 0)
    end = (rows - 1, cols - 1)
    if maze_array[start] == 1 or maze_array[end] == 1:
        return None  # no solution if start/end blocked
    
    queue = [(start, [start])]
    visited = set([start])
    moves = [(0,1), (1,0), (0,-1), (-1,0)]
    
    while queue:
        (r, c), path = queue.pop(0)
        if (r, c) == end:
            return path
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze_array[nr, nc] != 1 and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None

def count_solutions(maze, start=(0,0), end=None, limit=2):
    """
    Count up to 'limit' solutions using DFS.
    Returns the number of solutions found (stops counting after limit is reached).
    """
    maze_array = np.array(maze)
    rows, cols = maze_array.shape
    if end is None:
        end = (rows - 1, cols - 1)
    count = [0]
    
    def dfs(r, c, visited):
        if (r, c) == end:
            count[0] += 1
            return
        if count[0] >= limit:
            return
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze_array[nr, nc] != 1 and (nr, nc) not in visited):
                visited.add((nr, nc))
                dfs(nr, nc, visited)
                visited.remove((nr, nc))
    
    dfs(start[0], start[1], set([start]))
    return count[0]

def check_constraints(maze):
    """
    Checks for three constraints:
      1. Cells at 1-indexed odd,odd positions (i.e. indices 0,2,4,...) must be paths (0).
      2. The maze should have a unique solution.
      3. If a monster (3) is on the critical (BFS) solution path, at least one sword (2)
         must be reachable from the start (treating walls (1) and monsters (3) as obstacles).
    Returns a list of warning messages.
    """
    warnings = []
    maze_array = np.array(maze)
    rows, cols = maze_array.shape

    # Constraint 1: Check that cells at (odd,odd) positions (1-indexed) are paths (0).
    for i in range(0, rows, 2):
        for j in range(0, cols, 2):
            if maze_array[i, j] == 1:
                warnings.append(f"Cell ({i+1},{j+1}) should be a path (0) but is a wall (1).")

    # Solve the maze.
    sol = solve_maze(maze_array)
    if sol is None:
        warnings.append("No solution exists!")
    else:
        # Constraint 2: Check for uniqueness.
        sol_count = count_solutions(maze_array)
        if sol_count > 1:
            warnings.append(f"Multiple solutions exist (found at least {sol_count}).")
        
        # Constraint 3: If a monster is on the critical path, ensure a sword is reachable.
        if any(maze_array[r, c] == 3 for (r, c) in sol):
            # Define a helper function: search from start while treating walls and monsters as obstacles.
            def sword_available(maze_array):
                start = (0, 0)
                visited = {start}
                queue = [start]
                while queue:
                    r, c = queue.pop(0)
                    if maze_array[r, c] == 2:
                        return True  # Found a sword!
                    for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if maze_array[nr, nc] in (1, 3):  # Treat walls and monsters as obstacles.
                                continue
                            if (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                return False

            if not sword_available(maze_array):
                warnings.append("Critical path contains a monster but no reachable sword is available!")
    return warnings

#######################
# Plotting Function
#######################

def plot_maze(maze, ax=None, show_solution=True):
    """
    Plots the maze using matplotlib.
    Color scheme:
      0: White (path)
      1: Black (wall)
      2: Yellow (Sword / marker)
      3: Red (Monster / marker)
    Also plots the solution path if found.
    Additionally, highlights (even, even) cells (1-indexed) in magenta (as a reminder).
    """
    maze_array = np.array(maze)
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,8))
    
    colors = ['white', 'black', 'yellow', 'red']
    cmap = ListedColormap(colors)
    
    ax.imshow(maze_array, cmap=cmap, origin="upper", vmin=0, vmax=3)
    rows, cols = maze_array.shape
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
    ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
    
    # Add markers for cells with value 2 or 3
    for i in range(rows):
        for j in range(cols):
            if maze_array[i, j] == 2:
                ax.text(j, i, 'S', ha='center', va='center', color='black', fontweight='bold')
            elif maze_array[i, j] == 3:
                ax.text(j, i, 'M', ha='center', va='center', color='white', fontweight='bold')
    
    # Plot solution if requested
    if show_solution:
        sol = solve_maze(maze_array)
        if sol:
            ys, xs = zip(*sol)
            ax.plot(xs, ys, 'b-', linewidth=2, alpha=0.7)
            ax.plot(xs[0], ys[0], 'go', markersize=8)
            ax.plot(xs[-1], ys[-1], 'ro', markersize=8)
            ax.text(0.5, 0.01, "Solution Found", transform=ax.transAxes,
                    ha='center', va='bottom', color='green',
                    bbox=dict(facecolor='white', alpha=0.7))
        else:
            ax.text(0.5, 0.01, "No Solution Exists", transform=ax.transAxes,
                    ha='center', va='bottom', color='red',
                    bbox=dict(facecolor='white', alpha=0.7))
    
    # Highlight (even, even) cells (1-indexed -> indices 1,3,5,...) in magenta
    for i in range(1, rows, 2):
        for j in range(1, cols, 2):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=True, color='magenta', alpha=0.2))
    return ax

#######################
# Interactive Editor App
#######################

class MazePatternEditorApp:
    def __init__(self, root, patterns, file_path=None):
        self.root = root
        self.patterns = patterns  # list of numpy arrays
        self.file_path = file_path
        self.current_pattern_idx = 0

        # Register window close event
        # self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.title("Maze Pattern Editor")
        self.root.geometry("900x900")

        # Control frame at the top
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(fill=tk.X)
        
        # Using pattern from file
        ttk.Label(self.control_frame, text="File:").pack(side=tk.LEFT, padx=(0,1))
        ttk.Label(self.control_frame, text=os.path.splitext(os.path.basename(file_path))[0]).pack(side=tk.LEFT)

        # add a extending spacer
        ttk.Label(self.control_frame, text="").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Dropdown to select pattern
        ttk.Label(self.control_frame, text="Select Pattern:").pack(side=tk.LEFT, padx=(0,10))
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
        
        # Navigation buttons
        self.prev_button = ttk.Button(self.control_frame, text="Previous", command=self.prev_pattern)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button = ttk.Button(self.control_frame, text="Next", command=self.next_pattern)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # Save button
        self.save_button = ttk.Button(self.control_frame, text="Save Pattern", command=self.save_pattern)
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        # Index display label
        self.index_label = ttk.Label(self.control_frame, text=f"Pattern 1/{len(patterns)}")
        self.index_label.pack(side=tk.LEFT, padx=20)
        
        # Legend frame
        self.legend_frame = ttk.Frame(root, padding="5")
        self.legend_frame.pack(fill=tk.X)
        ttk.Label(self.legend_frame, text="Legend:").pack(side=tk.LEFT, padx=(0,10))
        # Create small colored canvases for legend items
        for text, color in [("Path (0)", "white"), ("Wall (1)", "black"),
                            ("Sword (2)", "yellow"), ("Monster (3)", "red")]:
            ttk.Label(self.legend_frame, text=text).pack(side=tk.LEFT, padx=(0,5))
            c = tk.Canvas(self.legend_frame, width=20, height=20, bg=color, highlightbackground="gray", highlightthickness=1)
            if text.startswith("Sword"):
                c.create_text(10,10, text="S", fill="black", font=("TkDefaultFont", 10, "bold"))
            elif text.startswith("Monster"):
                c.create_text(10,10, text="M", fill="white", font=("TkDefaultFont", 10, "bold"))
            c.pack(side=tk.LEFT, padx=(0,15))
        
        # Warning label (for constraint messages)
        self.warning_label = ttk.Label(root, text="", foreground="red", padding="5")
        self.warning_label.pack(fill=tk.X)
        
        # Create matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind mouse click event on the canvas for editing
        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)
        
        # Display the first pattern and update warnings
        self.update_plot()
        self.update_warnings()
        self.update_button_states()

    def on_closing(self):
        plt.close(self.fig)
        self.root.destroy()

    def update_plot(self):
        self.ax.clear()
        plot_maze(self.patterns[self.current_pattern_idx], self.ax)
        self.ax.set_title(f"Pattern {self.current_pattern_idx + 1}")
        self.pattern_selector.current(self.current_pattern_idx)
        self.index_label.config(text=f"Pattern {self.current_pattern_idx + 1}/{len(self.patterns)}")
        self.canvas.draw()
    
    def update_warnings(self):
        warnings = check_constraints(self.patterns[self.current_pattern_idx])
        if warnings:
            self.warning_label.config(text="\n".join(warnings), foreground="red")
        else:
            self.warning_label.config(text="No warnings.", foreground="green")
    
    def update_button_states(self):
        self.prev_button.config(state=tk.NORMAL if self.current_pattern_idx > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_pattern_idx < len(self.patterns) - 1 else tk.DISABLED)
    
    def on_pattern_selected(self, event):
        idx = self.pattern_selector.current()
        if 0 <= idx < len(self.patterns):
            self.current_pattern_idx = idx
            self.update_plot()
            self.update_warnings()
            self.update_button_states()
    
    def next_pattern(self):
        if self.current_pattern_idx < len(self.patterns) - 1:
            self.current_pattern_idx += 1
            self.update_plot()
            self.update_warnings()
            self.update_button_states()
    
    def prev_pattern(self):
        if self.current_pattern_idx > 0:
            self.current_pattern_idx -= 1
            self.update_plot()
            self.update_warnings()
            self.update_button_states()
    
    def on_canvas_click(self, event):
        # Only act if click is within the axes
        if event.inaxes != self.ax:
            return
        # Calculate cell indices from event coordinates
        if event.xdata is None or event.ydata is None:
            return
        col = int(round(event.xdata))
        row = int(round(event.ydata))
        pattern = self.patterns[self.current_pattern_idx]
        rows, cols = pattern.shape
        if 0 <= row < rows and 0 <= col < cols:
            # Cycle the cell's value: 0 -> 1 -> 2 -> 3 -> 0 ...
            old_val = pattern[row, col]

            # Left click (event.button == 1): cycle forward (0 -> 1 -> 2 -> 3 -> 0)
            if event.button == 1:
                new_val = (old_val + 1) % 4
            # Right click (event.button == 3): cycle backward (0 -> 3 -> 2 -> 1 -> 0)
            elif event.button == 3:
                new_val = (old_val - 1) % 4
            else:
                # Middle click or other button - do nothing
                return

            pattern[row, col] = new_val
            self.update_plot()
            self.update_warnings()
    
    def save_pattern(self):
        # APPEND the current pattern to a new file
        file_path = f"{os.path.splitext(self.file_path)[0]}_edited.txt"
        pattern = self.patterns[self.current_pattern_idx]
        try:
            with open(file_path, "a") as f:
                for row in pattern:
                    f.write(" ".join(map(str, row)) + "\n")
                f.write("\n")
            messagebox.showinfo("Save Pattern", f"Pattern saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Pattern", f"Error saving pattern: {str(e)}")

#######################
# Main Function
#######################

def main():
    try:
        # file_path = "input.txt"  # Input file with maze patterns
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument("file_path", help="Path to the input file with maze patterns")
        args = parser.parse_args()

        patterns = read_maze_patterns(args.file_path)
        if not patterns:
            print("No patterns found in the input file.")
            return
        root = tk.Tk()
        app = MazePatternEditorApp(root, patterns, args.file_path)
        root.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
