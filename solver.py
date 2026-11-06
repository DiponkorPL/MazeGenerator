from collections import deque
import heapq
import time


# Get valid Neighbors

def get_neighbors(maze, position):
    x, y = position
    movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []

    for dx, dy in movements:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] == 0:
            neighbors.append((nx, ny))

    return neighbors
#Reconstruct path from start to goal

def reconstruct_path(parent, goal):
    if goal not in parent:
        return []
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

# Bfs algorithm implementation

def bfs(maze, start, goal):
    start_time = time.perf_counter()
    queue = deque([start])
    parent = {start: None}
    explored = []
    while queue:
        current = queue.popleft()
        explored.append(current)
        if current == goal:
            break
        for neighbor in get_neighbors(maze, current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    path = reconstruct_path(parent, goal)
    elapsed_time = time.perf_counter() - start_time
    return path, explored, elapsed_time


# Manhattan distance heuristic function
def manhattan_distance(position, goal):
    x1, y1 = position
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)


# A* algorithm implementation

def a_star(maze, start, goal):
    start_time = time.time()
    priority_queue = []
    heapq.heappush(priority_queue, (manhattan_distance(start, goal), start))
    parent = {start: None}
    g_score = {start: 0}
    explored = []
    while priority_queue:
        current_f, current = heapq.heappop(priority_queue)

        if current_f != (g_score[current] + manhattan_distance(current, goal)):
            continue  # Skip if the f-score is outdated
        explored.append(current)
        if current == goal:
            break
        for neighbor in get_neighbors(maze, current):
            new_g_score = g_score[current] + 1  # Assuming cost between neighbors is 1
            if neighbor not in g_score or new_g_score < g_score[neighbor]:
                g_score[neighbor] = new_g_score
                parent[neighbor] = current
                h_score = manhattan_distance(neighbor, goal)
                f_score = new_g_score + h_score
                heapq.heappush(priority_queue, (f_score, neighbor))
    path = reconstruct_path(parent, goal)
    elapsed_time = time.time() - start_time
    return path, explored, elapsed_time