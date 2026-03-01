# Dynamic Pathfinding Agent

A Python-based graphical application that demonstrates **Informed Search Algorithms** in a dynamic, grid-based environment. The agent can navigate from a start point to a goal while obstacles appear in real-time, forcing the agent to re-calculate its path on the fly.

## 🚀 Features
* **User-Defined Grid:** Configure the number of rows and columns dynamically.
* **Search Algorithms:** * **A* Search:** Guaranteed shortest path using $f(n) = g(n) + h(n)$.
    * **Greedy Best-First Search:** Fast, heuristic-only search using $f(n) = h(n)$.
* **Heuristic Options:** Support for both **Manhattan** and **Euclidean** distance.
* **Interactive Map Editor:** Click to place/remove walls manually or generate random mazes.
* **Dynamic Re-planning:** Enable "Dynamic Mode" to watch the agent navigate while new obstacles spawn randomly.

## 🛠️ Installation & Requirements
This project uses Python 3 and the built-in `tkinter` library for the GUI. No external heavy dependencies like Pygame are required.

1.  **Ensure Python is installed:** [Download Python](https://www.python.org/downloads/)
2.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sheezahhumayun/Dyname-Pathfinding-Agent-with-A-and-GBFS.git]
    ```
3.  **Navigate to the folder:**
    ```bash
    cd Dyname-Pathfinding-Agent-with-A-and-GBFS
    ```

## 💻 How to Run
Run the application using the following command:
```bash
python pathfinder.py
```
## 📊 Visualizations
Yellow: Frontier (nodes in the priority queue).

Red: Visited nodes (explored).

Green Path: The final calculated path.


## 📝 Performance Metrics
The application tracks and displays:

Nodes Visited: Total nodes expanded during the search.

Path Cost: The total length of the final path.

Execution Time: Time taken to find the solution (in milliseconds).

## 3. Project Summary

| Algorithm | Heuristic | Optimality | Best Used For... |
| :--- | :--- | :--- | :--- |
| **A*** | Manhattan | Yes | Perfect grid navigation (4-way). |
| **A*** | Euclidean | Yes | Shortest line-of-sight path. |
| **Greedy BFS** | Either | No | Large maps where speed is more important than the shortest path. |
