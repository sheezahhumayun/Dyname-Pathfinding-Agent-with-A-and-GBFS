import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import time
import random
import math

# --- Configuration & Constants ---
CELL_SIZE = 25
COLORS = {
    "start": "#27ae60",      # Green
    "goal": "#c0392b",       # Red
    "wall": "#2c3e50",       # Dark Blue/Grey
    "empty": "#ecf0f1",      # Light Grey
    "visited": "#e74c3c",    # Soft Red
    "frontier": "#f1c40f",   # Yellow
    "path": "#2ecc71"        # Bright Green
}

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")
        
        # Grid Variables (Default)
        self.rows = 20
        self.cols = 20
        self.grid = {}
        self.start_node = (17, 10)
        self.goal_node = (10, 10)
        
        # State Variables
        self.running_dynamic = False
        self.agent_pos = None
        
        self.setup_gui()
        self.update_grid_size() # Initial build

    def setup_gui(self):
        # Sidebar for Controls
        sidebar = tk.Frame(self.root, padx=10, pady=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="Grid Settings", font=('Arial', 11, 'bold')).pack(anchor="w")
        
        # Row/Col Inputs
        size_frame = tk.Frame(sidebar)
        size_frame.pack(fill="x", pady=5)
        
        tk.Label(size_frame, text="Rows:").grid(row=0, column=0)
        self.row_entry = tk.Entry(size_frame, width=5)
        self.row_entry.insert(0, "20")
        self.row_entry.grid(row=0, column=1)
        
        tk.Label(size_frame, text="Cols:").grid(row=1, column=0)
        self.col_entry = tk.Entry(size_frame, width=5)
        self.col_entry.insert(0, "20")
        self.col_entry.grid(row=1, column=1)
        
        tk.Button(sidebar, text="Update Grid Size", command=self.update_grid_size).pack(fill="x", pady=2)

        tk.Label(sidebar, text="Algorithm & Heuristic", font=('Arial', 11, 'bold'), pady=10).pack(anchor="w")
        
        self.algo_var = tk.StringVar(value="A*")
        ttk.Combobox(sidebar, textvariable=self.algo_var, values=["A*", "Greedy BFS"]).pack(fill="x")

        self.heur_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(sidebar, textvariable=self.heur_var, values=["Manhattan", "Euclidean"]).pack(fill="x", pady=5)

        tk.Label(sidebar, text="Obstacle Density (%):").pack(anchor="w")
        self.density_scale = tk.Scale(sidebar, from_=0, to=50, orient=tk.HORIZONTAL)
        self.density_scale.set(30)
        self.density_scale.pack(fill="x")

        # Control Buttons
        tk.Button(sidebar, text="Generate Random Map", command=self.generate_random_map).pack(fill="x", pady=5)
        tk.Button(sidebar, text="Start Search (Static)", command=self.run_static_search).pack(fill="x", pady=5)
        self.dyn_btn = tk.Button(sidebar, text="Start Dynamic Mode", command=self.toggle_dynamic_mode, bg="#3498db", fg="white")
        self.dyn_btn.pack(fill="x", pady=5)
        tk.Button(sidebar, text="Clear Walls", command=self.clear_walls).pack(fill="x", pady=5)

        # Metrics Dashboard
        self.metrics_frame = tk.LabelFrame(sidebar, text="Metrics", padx=5, pady=5)
        self.metrics_frame.pack(fill="x", pady=10)
        self.nodes_lbl = tk.Label(self.metrics_frame, text="Nodes Visited: 0")
        self.nodes_lbl.pack(anchor="w")
        self.cost_lbl = tk.Label(self.metrics_frame, text="Path Cost: 0")
        self.cost_lbl.pack(anchor="w")
        self.time_lbl = tk.Label(self.metrics_frame, text="Time: 0ms")
        self.time_lbl.pack(anchor="w")

        # Canvas for Grid
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

    # --- Grid Management ---
    def update_grid_size(self):
        try:
            new_rows = int(self.row_entry.get())
            new_cols = int(self.col_entry.get())
            
            if new_rows < 5 or new_cols < 5:
                raise ValueError
            
            self.rows = new_rows
            self.cols = new_cols
            self.canvas.config(width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE)
            
            # Reposition Start/Goal for new size
            self.start_node = (17, 10)
            self.goal_node = (10,10)
            
            self.clear_walls()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers (min 5x5).")

    def clear_walls(self):
        self.grid = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[(r, c)] = "empty"
        self.grid[self.start_node] = "start"
        self.grid[self.goal_node] = "goal"
        self.draw_grid()

    def generate_random_map(self):
        self.clear_walls()
        density = self.density_scale.get() / 100
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in [self.start_node, self.goal_node]:
                    if random.random() < density:
                        self.grid[(r, c)] = "wall"
        self.draw_grid()

    def handle_click(self, event):
        c, r = event.x // CELL_SIZE, event.y // CELL_SIZE
        if (r, c) == self.start_node or (r, c) == self.goal_node:
            return
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[(r, c)] = "wall" if self.grid.get((r, c)) != "wall" else "empty"
            self.draw_grid()

    def draw_grid(self, visited=None, frontier=None, path=None):
        self.canvas.delete("all")
        for (r, c), type_ in self.grid.items():
            color = COLORS[type_]
            
            # Priority coloring for visualization
            if path and (r, c) in path and (r, c) not in [self.start_node, self.goal_node]:
                color = COLORS["path"]
            elif visited and (r, c) in visited and (r, c) not in [self.start_node, self.goal_node]:
                color = COLORS["visited"]
            elif frontier and (r, c) in frontier and (r, c) not in [self.start_node, self.goal_node]:
                color = COLORS["frontier"]
            
            x1, y1 = c * CELL_SIZE, r * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#bdc3c7")

    # --- Heuristics ---
    def get_heuristic(self, n1, n2):
        if self.heur_var.get() == "Manhattan":
            return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])
        return math.sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)

    # --- Search Logic ---
    def search(self, start, goal):
        start_time = time.perf_counter()
        algo = self.algo_var.get()
        
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        visited = []

        while frontier:
            _, current = heapq.heappop(frontier)
            visited.append(current)
            if current == goal: break

            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0] + dr, current[1] + dc)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                    if self.grid[neighbor] == "wall": continue
                    
                    new_cost = cost_so_far[current] + 1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        h = self.get_heuristic(neighbor, goal)
                        priority = (new_cost + h) if algo == "A*" else h
                        heapq.heappush(frontier, (priority, neighbor))
                        came_from[neighbor] = current

        end_time = time.perf_counter()
        path = []
        curr = goal
        if goal in came_from:
            while curr is not None:
                path.append(curr); curr = came_from[curr]
            path.reverse()
        
        self.nodes_lbl.config(text=f"Nodes Visited: {len(visited)}")
        self.cost_lbl.config(text=f"Path Cost: {max(0, len(path)-1)}")
        self.time_lbl.config(text=f"Time: {(end_time - start_time)*1000:.2f}ms")
        return path, visited, [f[1] for f in frontier]
 def run_static_search(self):
        path, visited, frontier = self.search(self.start_node, self.goal_node)
        if not path: messagebox.showinfo("Result", "No path found!")
        self.draw_grid(visited, frontier, path)

    # --- Dynamic Re-planning ---
    def toggle_dynamic_mode(self):
        if self.running_dynamic:
            self.running_dynamic = False
            self.dyn_btn.config(text="Start Dynamic Mode", bg="#3498db")
        else:
            self.running_dynamic = True
            self.dyn_btn.config(text="Stop Dynamic Mode", bg="#e67e22")
            self.agent_pos = self.start_node
            self.dynamic_step()

    def dynamic_step(self):
        if not self.running_dynamic: return
        path, visited, frontier = self.search(self.agent_pos, self.goal_node)
        
        if not path or len(path) < 2:
            if self.agent_pos == self.goal_node:
                messagebox.showinfo("Success", "Goal Reached!")
            else:
                messagebox.showwarning("Blocked", "Path is obstructed!")
            self.toggle_dynamic_mode()
            return

        self.agent_pos = path[1]
        
        # Chance to spawn obstacle
        if random.random() < 0.15: # 15% chance per step
            r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if (r, c) not in [self.agent_pos, self.goal_node] and self.grid[(r, c)] == "empty":
                self.grid[(r, c)] = "wall"

        self.draw_grid(visited, frontier, path)
        # Draw Agent
        x1, y1 = self.agent_pos[1]*CELL_SIZE+4, self.agent_pos[0]*CELL_SIZE+4
        x2, y2 = x1+CELL_SIZE-8, y1+CELL_SIZE-8
        self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black", width=2)
        
        self.root.after(150, self.dynamic_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
