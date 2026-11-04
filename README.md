# Python Maze Generator

A random Maze Generator built using Python and the **Depth-First Search (DFS)** algorithm.

## Features

- Random Maze Generation
- DFS Algorithm
- Recursive Backtracking (implemented using a Stack)
- Three Difficulty Levels:
  - Easy
  - Medium
  - Hard
- Randomized Maze Paths

## Technologies Used

- Python 3
- Random Module
- Data Structures (2D List and Stack)
- Depth-First Search (DFS)

## How It Works

The project uses the Depth-First Search algorithm to generate random mazes.

1. Initially, all cells are marked as walls.
2. The algorithm starts from the starting position.
3. It checks four possible directions.
4. A random unvisited neighbor is selected.
5. The wall between the current cell and the selected neighbor is removed.
6. If no unvisited neighbor exists, the algorithm backtracks using a stack.
7. The process continues until the stack becomes empty.

## Difficulty Levels

| Difficulty | Width | Height |
|---|---:|---:|
| Easy | 21 | 21 |
| Medium | 31 | 21 |
| Hard | 41 | 31 |

## Installation

Clone the repository:

```bash
git clone https://github.com/DiponkorPL/MazeGenerator.git
```

Navigate to the project directory:

```bash
cd Python-Maze-Generator
```

Run the project:

```bash
python main.py
```
