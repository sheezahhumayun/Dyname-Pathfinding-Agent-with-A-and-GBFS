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
