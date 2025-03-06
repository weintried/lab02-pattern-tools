import random
import matplotlib.pyplot as plt
import numpy as np

def plot_maze(maze, solution_path=None):
    """
    Plots the maze using matplotlib with custom colors for different elements.
    0: Path (white)
    1: Wall (black)
    2: Sword (gold)
    3: Monster (red)
    
    If solution_path is provided, it will be highlighted on the maze.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Create a custom colormap for the maze elements
    colors = ['white', 'black', 'gold', 'red']
    cmap = plt.matplotlib.colors.ListedColormap(colors)
    
    # Display the maze with custom colormap
    im = ax.imshow(maze, cmap=cmap, vmin=0, vmax=3, origin="upper")
    
    # Get the shape of the maze
    rows, cols = np.array(maze).shape
    
    # Set major ticks at grid cell boundaries
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    
    # Turn on grid for minor ticks
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
    
    # Remove major ticks
    ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
    
    # Highlight the solution path if provided
    if solution_path:
        # Extract the coordinates for the path line
        path_y = [pos[0] for pos in solution_path]
        path_x = [pos[1] for pos in solution_path]
        
        # Plot the path with a blue line with markers
        ax.plot(path_x, path_y, 'b-', linewidth=2, alpha=0.7)
        ax.plot(path_x, path_y, 'bo', markersize=4, alpha=0.5)
        
        # Highlight start and end points
        ax.plot(path_x[0], path_y[0], 'go', markersize=10, label='Start')  # Green for start
        ax.plot(path_x[-1], path_y[-1], 'mo', markersize=10, label='Finish')  # Magenta for finish
    
    # Create legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='white', edgecolor='gray', label='Path (0)'),
        Patch(facecolor='black', edgecolor='gray', label='Wall (1)'),
        Patch(facecolor='gold', edgecolor='gray', label='Sword (2)'),
        Patch(facecolor='red', edgecolor='gray', label='Monster (3)')
    ]
    
    # Add solution path to legend if provided
    if solution_path:
        legend_elements.extend([
            plt.Line2D([0], [0], color='blue', lw=2, label='Solution Path'),
            plt.Line2D([0], [0], marker='o', color='green', label='Start', 
                      markerfacecolor='green', markersize=8),
            plt.Line2D([0], [0], marker='o', color='magenta', label='Finish', 
                      markerfacecolor='magenta', markersize=8)
        ])
    
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), 
              ncol=4, fancybox=True)
    
    plt.tight_layout()
    plt.show()

def export_maze_to_txt(maze, filename="maze.txt", transpose=False, export_flat=False, mode='w'):
    """
    Exports the maze to a text file for easier use in other programs.
    
    Args:
        maze: The maze to export
        filename: Name of the output file
        transpose: If True, transpose the maze (rows become columns)
    """
    if transpose:
        # Create transposed maze
        transposed_maze = [[maze[j][i] for j in range(len(maze))] for i in range(len(maze[0]))]
        
        with open(filename, mode) as f:
            for row in transposed_maze:
                f.write(' '.join(map(str, row)) + '\n')
            f.write('\n')
    else:
        with open(filename, mode) as f:
            for row in maze:
                f.write(' '.join(map(str, row)) + '\n')
            f.write('\n')
    
    print(f"Maze exported to {filename}{' (transposed)' if transpose else ''}")

    if export_flat:
        # Also export as flat list for direct use in the testbench
        base_name = filename.split('.')[0]
        with open(f"{base_name}_flat.txt", mode) as f:
            if transpose:
                # Create transposed maze as flat list
                transposed_maze = [[maze[j][i] for j in range(len(maze))] for i in range(len(maze[0]))]
                flat_maze = [cell for row in transposed_maze for cell in row]
                f.write(','.join(map(str, flat_maze)))
            else:
                flat_maze = [cell for row in maze for cell in row]
                f.write(','.join(map(str, flat_maze)))
            f.write('\n')

def find_accessible_cells(maze, start_pos):
    """
    Uses BFS to find all cells accessible from the starting position.
    Returns a list of (row, col) coordinates that are accessible.
    """
    N = len(maze)
    visited = [[False for _ in range(N)] for _ in range(N)]
    queue = [start_pos]
    visited[start_pos[0]][start_pos[1]] = True
    accessible = [start_pos]
    
    # Directions: right, down, left, up
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        r, c = queue.pop(0)
        
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (0 <= nr < N and 0 <= nc < N and 
                not visited[nr][nc] and maze[nr][nc] != 1):  # Not a wall
                visited[nr][nc] = True
                queue.append((nr, nc))
                accessible.append((nr, nc))
    
    return accessible

def find_solution_path(maze):
    """
    Finds the solution path from start (0,0) to finish (16,16) in the maze.
    Returns a list of (row, col) coordinates that make up the path.
    """
    N = len(maze)
    visited = [[False for _ in range(N)] for _ in range(N)]
    path = []
    
    def dfs(r, c):
        if r < 0 or r >= N or c < 0 or c >= N or visited[r][c] or maze[r][c] == 1:
            return False
        
        visited[r][c] = True
        path.append((r, c))
        
        # If we've reached the finish
        if r == N-1 and c == N-1:
            return True
        
        # Try all four directions
        if (dfs(r+1, c) or dfs(r, c+1) or dfs(r-1, c) or dfs(r, c-1)):
            return True
            
        # Backtrack if this position doesn't lead to a solution
        path.pop()
        return False
    
    dfs(0, 0)
    return path

def generate_maze_with_entities(sword_count=1, monster_count=1, monster_on_path_prob=0.5, sword_on_path_prob=0.3):
    """
    Generates a 17x17 maze with paths (0), walls (1), swords (2), and monsters (3).
    Ensures that the maze is solvable with varied scenarios:
    - There is one path from start to finish
    - Monsters might be on the critical path with probability monster_on_path_prob
    - If a monster is on the critical path, at least one sword is accessible before it
    - Swords can be on or off the critical path (controlled by sword_on_path_prob)
    
    Args:
        sword_count: Number of swords to place in the maze
        monster_count: Number of monsters to place in the maze
        monster_on_path_prob: Probability (0-1) of placing a monster on the critical path
        sword_on_path_prob: Probability (0-1) of placing swords directly on the critical path
                           (lower values force more detours to collect swords)
    """
    # Generate the basic maze structure with 0s and 1s (inverted from original)
    maze_17 = generate_random_maze_17x17()
    
    # Invert the maze values to match the lab spec (0=path, 1=wall)
    for r in range(len(maze_17)):
        for c in range(len(maze_17[0])):
            maze_17[r][c] = 1 - maze_17[r][c]
    
    # Find the solution path
    solution_path = find_solution_path(maze_17)
    
    # Make a copy of the path we can modify
    path_copy = solution_path.copy()
    
    # Remove start and end positions from potential entity placements
    path_copy.remove((0, 0))  # Start
    path_copy.remove((16, 16))  # End
    
    # Decide whether to place monsters on the critical path
    monsters_on_critical_path = random.random() < monster_on_path_prob
    monster_positions = []
    
    # Find all accessible cells (using BFS from start)
    accessible_cells = find_accessible_cells(maze_17, (0, 0))
    
    # Place monsters
    if monster_count > 0:
        if monsters_on_critical_path:
            # Place at least one monster on the critical path (in the latter half)
            potential_monster_positions = path_copy[len(path_copy)//2:]
            
            if potential_monster_positions:
                pos = random.choice(potential_monster_positions)
                r, c = pos
                maze_17[r][c] = 3  # Monster
                monster_positions.append(pos)
                potential_monster_positions.remove(pos)
                path_copy.remove(pos)
                monster_count -= 1
                
                # Find all path positions before the first monster
                first_monster_idx = solution_path.index(pos)
                pre_monster_positions = solution_path[1:first_monster_idx]  # Exclude start
                
                # Decide whether to place the required sword on or off the critical path
                if pre_monster_positions and random.random() >= sword_on_path_prob:
                    # Place sword OFF the critical path (forcing a detour)
                    
                    # Find accessible cells that are not on the critical path
                    accessible_before_monster = []
                    # Do a BFS from start to find all accessible positions before monster
                    temp_maze = [row[:] for row in maze_17]  # Make a copy
                    # Block the monster position to prevent BFS from going past it
                    temp_maze[pos[0]][pos[1]] = 1  
                    accessible_before_monster = find_accessible_cells(temp_maze, (0, 0))
                    
                    # Remove cells that are on the critical path
                    detour_cells = [cell for cell in accessible_before_monster 
                                  if cell not in solution_path and temp_maze[cell[0]][cell[1]] == 0]
                    
                    if detour_cells:
                        # Place sword in a detour location
                        sword_pos = random.choice(detour_cells)
                        r, c = sword_pos
                        maze_17[r][c] = 2  # Sword
                        sword_count -= 1
                    else:
                        # Fall back to placing on critical path if no detour available
                        if pre_monster_positions:
                            sword_pos = random.choice(pre_monster_positions)
                            r, c = sword_pos
                            maze_17[r][c] = 2  # Sword
                            if sword_pos in path_copy:
                                path_copy.remove(sword_pos)
                            sword_count -= 1
                else:
                    # Place sword ON the critical path (direct route)
                    if pre_monster_positions:
                        sword_pos = random.choice(pre_monster_positions)
                        r, c = sword_pos
                        maze_17[r][c] = 2  # Sword
                        if sword_pos in path_copy:
                            path_copy.remove(sword_pos)
                        sword_count -= 1
        
        # Place remaining monsters randomly (either on path or accessible areas)
        for _ in range(monster_count):
            # 30% chance to place on the critical path if allowed
            if path_copy and random.random() < 0.3 and monsters_on_critical_path:
                pos = random.choice(path_copy)
                r, c = pos
                maze_17[r][c] = 3  # Monster
                monster_positions.append(pos)
                path_copy.remove(pos)
            else:
                # Place monster in an accessible area (not on the critical path)
                non_path_accessible = [cell for cell in accessible_cells 
                                     if cell not in solution_path and maze_17[cell[0]][cell[1]] == 0]
                if non_path_accessible:
                    pos = random.choice(non_path_accessible)
                    r, c = pos
                    maze_17[r][c] = 3  # Monster
                    monster_positions.append(pos)
                    accessible_cells.remove(pos)
    
    # Place swords
    for _ in range(sword_count):
        # If monsters are on the critical path, ensure there's at least one sword before
        if monster_positions and any(pos in solution_path for pos in monster_positions) and sword_count == 1:
            # Find the first monster on the path
            path_monsters = [pos for pos in monster_positions if pos in solution_path]
            first_monster_idx = min([solution_path.index(pos) for pos in path_monsters])
            pre_monster_positions = solution_path[1:first_monster_idx]  # Exclude start
            
            # Decide whether to place sword on or off the critical path
            if pre_monster_positions and random.random() >= sword_on_path_prob:
                # Try to place sword OFF the critical path (forcing a detour)
                temp_maze = [row[:] for row in maze_17]
                
                # Block all monsters on the path to prevent going past them
                for m_pos in path_monsters:
                    temp_maze[m_pos[0]][m_pos[1]] = 1
                
                # Find all accessible cells before the monster
                accessible_before_monster = find_accessible_cells(temp_maze, (0, 0))
                
                # Remove cells that are on the critical path
                detour_cells = [cell for cell in accessible_before_monster 
                              if cell not in solution_path and temp_maze[cell[0]][cell[1]] == 0]
                
                if detour_cells:
                    # Place sword in a detour location
                    sword_pos = random.choice(detour_cells)
                    r, c = sword_pos
                    maze_17[r][c] = 2  # Sword
                    continue
            
            # Fall back to placing on critical path
            if pre_monster_positions:
                pos = random.choice(pre_monster_positions)
                r, c = pos
                maze_17[r][c] = 2  # Sword
                continue
        
        # Otherwise, place swords randomly throughout accessible areas
        if path_copy and random.random() < sword_on_path_prob:
            # Place on critical path
            pos = random.choice(path_copy)
            r, c = pos
            maze_17[r][c] = 2  # Sword
            path_copy.remove(pos)
        else:
            # Place sword in an accessible area (not on the critical path)
            non_path_accessible = [cell for cell in accessible_cells 
                                 if cell not in solution_path and maze_17[cell[0]][cell[1]] == 0]
            if non_path_accessible:
                pos = random.choice(non_path_accessible)
                r, c = pos
                maze_17[r][c] = 2  # Sword
                accessible_cells.remove(pos)
    
    return maze_17, solution_path, monster_positions

def generate_random_maze_17x17():
    """
    Generates a 17x17 maze pattern that, if embedded in a 19x19 grid,
    would be fully enclosed by walls. We do this by:
      1) Building a 19x19 grid (indices 0..18),
      2) Forcing the outer ring to be walls (0),
      3) Carving passages in the 17x17 interior with a DFS,
      4) Returning only the 17x17 inner portion.
    
    Returns:
      A 17x17 list of lists (each entry 0=wall or 1=open).
    """
    N = 19  # total size
    maze_19 = [[0]*N for _ in range(N)]
    
    # (1) Outer ring stays walls => row=0, row=18, col=0, col=18 are all 0.
    #     We'll carve only in rows 1..17, cols 1..17.

    # (2) Mark interior odd-row, odd-col squares as passable "cells"
    #     i.e. (r,c) in {1,3,5,7,9,11,13,15,17}.
    for r in range(1, N-1):
        for c in range(1, N-1):
            if (r % 2 == 1) and (c % 2 == 1):
                maze_19[r][c] = 1  # cell center

    # We have 9 odd indices in [1..17], so we treat that as a 9x9 cell grid:
    # cell_row = (r-1)//2, cell_col = (c-1)//2, each in [0..8].
    visited = [[False]*9 for _ in range(9)]

    def get_neighbors(cr, cc):
        neighbors = []
        if cr > 0:  neighbors.append((cr-1, cc))
        if cr < 8:  neighbors.append((cr+1, cc))
        if cc > 0:  neighbors.append((cr, cc-1))
        if cc < 8:  neighbors.append((cr, cc+1))
        return neighbors

    # (3) Random DFS over the 9x9 cell graph
    stack = [(0, 0)]   # Start from cell(0,0) => (r=1, c=1) in 19x19
    visited[0][0] = True

    while stack:
        cr, cc = stack[-1]
        unvisited_neighbors = [
            (nr, nc) for (nr, nc) in get_neighbors(cr, cc)
            if not visited[nr][nc]
        ]
        if unvisited_neighbors:
            nr, nc = random.choice(unvisited_neighbors)
            visited[nr][nc] = True

            # Carve a passage in the 19x19 between (cr,cc) and (nr,nc)
            r1, c1 = 2*cr + 1, 2*cc + 1
            r2, c2 = 2*nr + 1, 2*nc + 1
            mid_r, mid_c = (r1 + r2)//2, (c1 + c2)//2

            maze_19[mid_r][mid_c] = 1

            stack.append((nr, nc))
        else:
            stack.pop()

    # (4) Discard the outermost ring, return only the 17x17 interior
    #     That is rows 1..17, cols 1..17 of maze_19.
    maze_17 = []
    for row_idx in range(1, N-1):
        maze_17.append(maze_19[row_idx][1:N-1])

    return maze_17

if __name__ == "__main__":
    # # Generate a maze with varied settings
    # sword_count = np.random.randint(1, 3)
    # monster_count = np.random.randint(1, 3)
    # monster_on_path_prob = 0.5
    # sword_on_path_prob = 0.5

    # maze, solution_path, monster_positions = generate_maze_with_entities(
    #     sword_count=sword_count, 
    #     monster_count=monster_count,
    #     monster_on_path_prob=monster_on_path_prob,
    #     sword_on_path_prob=sword_on_path_prob
    # )
    
    # # Print details about the solution
    # print(f"Solution path length: {len(solution_path)}")
    # print(f"{sword_count=}, {monster_count=}")
    
    # # Check if any monsters are on the critical path
    # monsters_on_path = [pos for pos in monster_positions if pos in solution_path]
    # if monsters_on_path:
    #     print(f"Monsters on critical path: {len(monsters_on_path)} at positions {monsters_on_path}")
        
    #     # Verify if there's a sword before the first monster
    #     first_monster_idx = min([solution_path.index(pos) for pos in monsters_on_path])
        
    #     # Check for swords on the critical path
    #     sword_on_path = False
    #     for i in range(1, first_monster_idx):
    #         r, c = solution_path[i]
    #         if maze[r][c] == 2:  # Sword
    #             sword_on_path = True
    #             print(f"Sword found on critical path at position {solution_path[i]}")
    #             break
        
    #     if not sword_on_path:
    #         # Check if there's a sword reachable via detour
    #         temp_maze = [row[:] for row in maze]
    #         # Block the first monster
    #         first_monster = monsters_on_path[0]
    #         temp_maze[first_monster[0]][first_monster[1]] = 1
            
    #         # Find accessible cells before monster
    #         accessible_cells = find_accessible_cells(temp_maze, (0, 0))
            
    #         # Find swords in accessible cells
    #         detour_swords = []
    #         for cell in accessible_cells:
    #             r, c = cell
    #             if maze[r][c] == 2:  # Sword
    #                 detour_swords.append(cell)
            
    #         if detour_swords:
    #             print(f"Swords requiring detour: {len(detour_swords)} at positions {detour_swords}")
    #         else:
    #             print("WARNING: No swords accessible before monster!")
    # else:
    #     print("No monsters on critical path - no sword required for solution")

    # # Check for roads on (even, even) positions (1-indexed)
    # even_even_roads = []
    # for r in range(0, 17):
    #     for c in range(0, 17):
    #         # Convert to 1-indexed for checking
    #         r1 = r + 1
    #         c1 = c + 1
    #         if r1 % 2 == 0 and c1 % 2 == 0 and maze[r][c] == 0:  # Road (0)
    #             even_even_roads.append((r, c))
    
    # if even_even_roads:
    #     print(f"Found {len(even_even_roads)} roads at even-even positions (1-indexed): {even_even_roads}")
    # else:
    #     print("No roads at even-even positions (1-indexed)")

    # # Plot the maze and solution path
    # plot_maze(maze, solution_path)

    # # Export maze to text file
    # export_maze_to_txt(maze, filename="maze.txt", transpose=True, export_flat=True)



    # Generate N patterns and categorize them
    # N = 10
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("num_patterns", type=int, nargs="?", default=10, help="Number of patterns to generate")
    args = parser.parse_args()
    N = args.num_patterns

    categories = {
        "no_swords_no_monsters": [],
        "only_swords": [],
        "swords_and_monsters": [],
        "detour_swords": []
    }

    for i in range(N):
        print(f"Generating pattern {i+1}/{N}...")
        # Randomize parameters for variety
        sword_count = random.randint(1, 3)
        monster_count = random.randint(1, 3)
        monster_on_path_prob = random.uniform(0.4, 0.8)
        sword_on_path_prob = random.uniform(0.3, 0.7)

        # Generate maze
        maze, solution_path, monster_positions = generate_maze_with_entities(
            sword_count=sword_count, 
            monster_count=monster_count,
            monster_on_path_prob=monster_on_path_prob,
            sword_on_path_prob=sword_on_path_prob
        )
        
        # Check if any monsters are on the critical path
        monsters_on_path = [pos for pos in monster_positions if pos in solution_path]
        
        # Find swords on critical path
        swords_on_path = []
        for pos in solution_path:
            r, c = pos
            if maze[r][c] == 2:  # Sword
                swords_on_path.append(pos)
        
        # Determine category
        category = None
        
        if not monsters_on_path:
            if not swords_on_path:
                category = "no_swords_no_monsters"
            else:
                category = "only_swords"
        else:
            # There are monsters on path - check if solvable
            first_monster_idx = min([solution_path.index(pos) for pos in monsters_on_path])
            
            # Check for swords on the critical path before the monster
            critical_path_sword_before_monster = False
            for pos in swords_on_path:
                if solution_path.index(pos) < first_monster_idx:
                    critical_path_sword_before_monster = True
                    category = "swords_and_monsters"
                    break
            
            if not critical_path_sword_before_monster:
                # Check for detour swords
                temp_maze = [row[:] for row in maze]
                # Block the first monster
                first_monster = monsters_on_path[0]
                temp_maze[first_monster[0]][first_monster[1]] = 1
                
                # Find accessible cells before monster
                accessible_cells = find_accessible_cells(temp_maze, (0, 0))
                
                # Find swords in accessible cells
                detour_swords = []
                for cell in accessible_cells:
                    r, c = cell
                    if maze[r][c] == 2:  # Sword
                        detour_swords.append(cell)
                
                if detour_swords:
                    category = "detour_swords"
                else:
                    # Not solvable - no sword before monster
                    category = None
        
        # Save the pattern if it's valid
        if category:
            pattern_num = len(categories[category]) + 1
            # filename = f"{category}_{pattern_num}.txt"
            filename = category + ".txt"
            
            # Export maze to text file
            export_maze_to_txt(maze, filename=filename, transpose=True, export_flat=False, mode='a')
            categories[category].append(filename)
            
            print(f"Saved pattern to {filename} (Category: {category})")
        else:
            print("Pattern discarded (unsolvable)")

    # Print summary
    print("\nGeneration Summary:")
    for category, files in categories.items():
        print(f"{category}: {len(files)} patterns")
