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
