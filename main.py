import pygame
import time
from maze_generator import Maze_Generator
from visualizer import MazeVisualizer
from solver import solve_bfs, solve_dfs, solve_a_star

pygame.init()

Screen_width = 800
Screen_height = 600
Cell_size = 20
screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("Maze lab")

clock = pygame.time.Clock()

generator = Maze_Generator(width=31, height=21)
visualizer = MazeVisualizer(generator, screen, cell_size=Cell_size)
button = visualizer.get_button_rect()

maze, start,goal = generator.generate()

player = start
mode = "Ready"
algorithm = None
status = "Choose Human or AI"

moves = 0
human_start_time = None
human_elapsed_time = 0.0
solver_elapsed_time = 0.0

exlored = []
path = []

solving = False
animation_step = 0
animation_counter = 0
animation_delay = 2  # Delay in frames between animation steps

def reset_game():
    global maze, start, goal
    global player, mode, algorithm, status
    global moves, human_start_time, human_elapsed_time
    global solver_elapsed_time, explored, path
    global solving, animation_step, animation_counter

    maze, start, goal = generator.generate()

    player = start
    mode = "Ready"
    algorithm = None
    status = "Choose Human or AI"

    moves = 0
    human_start_time = None
    human_elapsed_time = 0.0
    solver_elapsed_time = 0.0

    explored = []
    path = []

    solving = False
    animation_step = 0
    animation_counter = 0

def start_ai_solver(solver_function,algorithm_name):
    global mode,algorithm, status
    global exlored, path, solver_elapsed_time
    global solving, animation_step, animation_counter
    global moves, player

    mode = "AI"
    algorithm = algorithm_name
    status = f"Solving with {algorithm_name}..."

    player = start
    moves = 0
    path,explored, solver_elapsed_time = solver_function(maze, start, goal)
    animation_step = 0
    animation_counter = 0
    solving = bool(path)  # Set solving to True if a path is found, False otherwise

    if not path:
        status = "No path found by the AI solver."
    else:
        status = f"AI solver found a path with {len(path)} steps in {solver_elapsed_time:.2f} seconds."

def move_player(dx,dy):
    global player,moves, status, human_elapsed_time
    if mode != "Human" or status =="You reached the goal!":
        return
    x,y = player
    nx = x + dx 
    ny = y + dy
    if 0 <= nx < generator.width and 0 <= ny < generator.height and maze[ny][nx] == 0:
        player = (nx, ny)
        moves += 1
        if player == goal:
            status = "You reached the goal!"
            if human_start_time is not None:
                human_elapsed_time = time.time() - human_start_time

running = True

