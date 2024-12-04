# MySokoban - AI-Powered Sokoban Solver
MySokoban is an AI-based project that solves and simulates the Sokoban puzzle using search algorithms such as Breadth-First Search (BFS), Depth-First Search (DFS), A*, Backtracking, and Simulated Annealing.
## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies](#technologies)
4. [How It Works](#how-it-works)
5. [Algorithms Implemented](#algorithms-implemented)
6. [Getting Started](#getting-started)
7. [Future Improvements](#future-improvements)
8. [Authors](#authors)
## Overview
Sokoban is a classic puzzle game developed in the 1980s in Japan. This project combines the logical challenges of Sokoban with AI algorithms to:
- Solve Sokoban puzzles automatically.
- Simulate gameplay interactively.
- Evaluate the performance of various AI algorithms.
## Features
- **Interactive Gameplay:** Play manually or watch AI solve puzzles.
- **Multiple AI Algorithms:** BFS, DFS, A*, Simulated Annealing, Backtracking.
- **Performance Metrics:** Compare steps, time, and efficiency.
- **Graphical Interface:** Pygame-based visualization.
## Technologies
- Python 3.10+
- Pygame
- Tkinter
- Matplotlib
- Pandas
- Jupyter Notebook
## How It Works
1. **Game Representation:** Levels are represented as 2D matrices with symbols like `@`, `$`, `.` for workers, boxes, and goals.
2. **State Management:** Track the positions of all entities and update based on actions.
3. **Algorithm Execution:** Use selected AI algorithms to find and display optimal solutions.
## Algorithms Implemented
- **Breadth-First Search (BFS):** Explores all possibilities level by level.
- **Depth-First Search (DFS):** Focuses on one path deeply before backtracking.
- **A***: Combines cost-so-far with heuristic estimates for optimal paths.
- **Simulated Annealing:** Uses probabilistic techniques to escape local optima.
- **Backtracking:** Systematically explores and backtracks on failure.
## Getting Started
Clone the repository:
   ```bash
   git clone https://github.com/ToiLaBao2004/MySokoban.git
   cd MySokoban
   ```
## Future Improvements
- Enhance heuristic functions for A*.
- Introduce custom map generation.
- Add advanced deadlock detection.
## Authors
- **Nguyễn Hoài Bảo** - [GitHub](https://github.com/ToiLaBao2004)
- **Phan Phúc Hảo** - [GitHub](https://github.com/haophan361)
- **Nguyễn Võ Cát Tường** - [GitHub](https://github.com/Hotvitlonxaome)
## How to Play
You can use the arrow keys ↑ ↓ ← → to play the game.<br>
Press the Z button to go back to the previous position.<br>
Press the B button to solve with BFS.<br>
Press the D button to solve with DFS.<br>
Press the A button to solve with A*.<br>
Press the K button to solve with BACKTRACKING.<br>
Press the S button to solve with SIMULATED ANNEALING.<br>
The console will display the solution, solving time, and the number of states explored.<br>
![Sokoban](https://github.com/user-attachments/assets/c2a94d8d-94b4-4d7f-b9ec-754474aecea0)