import pygame
import time
from maze import maze_Generator
from visualizer import MazeVisualizer
from solver import bfs, a_star

pygame.init()

Screen_width = 1000
Screen_height = 700
Cell_size = 20
screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("Maze lab")

clock = pygame.time.Clock()
generator = maze_Generator(width=31, height=21)

maze, start,goal = generator.generate()
visualizer = MazeVisualizer(screen, maze, start, goal)

buttons = {
    "New Maze": pygame.Rect(650, 100, 150, 40),
    "Human": pygame.Rect(650, 155, 150, 40),
    "BFS": pygame.Rect(650, 210, 150, 40),
    "A*": pygame.Rect(650, 265, 150, 40),
    "Reset": pygame.Rect(650, 320, 150, 40)
}

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
animation_delay = 2  # Delay in frames between animation steps

def reset_game():
    global maze, start, goal
    global player, mode, algorithm, status
    global moves, human_start_time, human_elapsed_time
    global solver_elapsed_time, explored, path
    global solving, animation_step, animation_counter

    maze, start, goal = generator.generate()

    visualizer.maze = maze
    visualizer.start = start
    visualizer.goal = goal
    visualizer.rows = len(maze)
    visualizer.cols = len(maze[0])

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

def start_human_mode():
    global player, mode, algorithm, status, moves
    global human_start_time, human_elapsed_time
    global solver_elapsed_time, explored, path, solving

    player = start
    mode = "Human"
    algorithm = None
    status = "Use Arrow Keys or WASD"

    moves = 0

    human_start_time = time.perf_counter()
    human_elapsed_time = 0.0
    solver_elapsed_time = 0.0

    explored = []
    path = []
    solving = False

def start_ai_solver(solver_function,algorithm_name):
    global mode,algorithm, status
    global explored, path, solver_elapsed_time
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

font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

# !draw button function

def draw_button(text, rect, color):
    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=8
    )
    label = font.render(text, True, (255, 255, 255))
    screen.blit(
        label,
        label.get_rect(center=rect.center)
    )

def draw_interface():
    screen.fill((18, 22, 32))
    title = font.render(
        "SMART MAZE LAB",
        True,
        (255, 255, 255)
    )
    screen.blit(title, (650, 35))
    draw_button(
        "New Maze",
        buttons["New Maze"],
        (40, 100, 170)
    )
    draw_button(
        "Human",
        buttons["Human"],
        (35, 130, 85)
    )
    draw_button(
        "BFS Solve",
        buttons["BFS"],
        (40, 105, 175)
    )
    draw_button(
        "A* Solve",
        buttons["A*"],
        (125, 75, 175)
    )
    draw_button(
        "Reset",
        buttons["Reset"],
        (75, 83, 104)
    )
    screen.blit(
        small_font.render(
            f"Mode: {mode}",
            True,
            (255, 255, 255)
        ),
        (650, 400)
    )
    screen.blit(
        small_font.render(
            f"Algorithm: {algorithm or 'None'}",
            True,
            (255, 255, 255)
        ),
        (650, 430)
    )
    screen.blit(
        small_font.render(
            f"Moves: {moves}",
            True,
            (255, 255, 255)
        ),
        (650, 460)
    )
    screen.blit(
        small_font.render(
            f"Time: {solver_elapsed_time:.5f}s",
            True,
            (255, 255, 255)
        ),
        (650, 490)
    )
    screen.blit(
        small_font.render(
            f"Path Length: {max(0, len(path) - 1)}",
            True,
            (255, 255, 255)
        ),
        (650, 520)
    )
    screen.blit(
        small_font.render(
            f"Explored: {len(explored)}",
            True,
            (255, 255, 255)
        ),
        (650, 550)
    )
    status_text = small_font.render(
        status[:42],
        True,
        (100, 220, 160)
    )
    screen.blit(status_text, (650, 590))

running = True

while running:
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if buttons["New Maze"].collidepoint(mouse_pos):
                    reset_game()
                elif buttons["Human"].collidepoint(mouse_pos):
                    start_human_mode()
                elif buttons["BFS"].collidepoint(mouse_pos):
                    start_ai_solver(bfs, "BFS")
                elif buttons["A*"].collidepoint(mouse_pos):
                    start_ai_solver(a_star, "A*")
                elif buttons["Reset"].collidepoint(mouse_pos):
                    reset_game()

        # Keyboard Controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if mode == "Human":
                if event.key in (pygame.K_UP, pygame.K_w):
                    move_player(0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    move_player(0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    move_player(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_player(1, 0)

    # 2. Human Timer
    if mode == "Human" and human_start_time is not None:
        if status == "You reached the goal!":
            display_time = human_elapsed_time
        else:
            display_time = time.perf_counter() - human_start_time
    elif mode == "AI":
        display_time = solver_elapsed_time
    else:
        display_time = 0.0

    # 3. AI Animation
    if solving:
        animation_counter += 1

        if animation_counter >= animation_delay:
            animation_counter = 0
            animation_step += 1
            total_steps = len(explored) + len(path)

            if animation_step >= total_steps:
                animation_step = total_steps
                solving = False
                status = f"{algorithm} completed! Shortest path: {len(path) - 1} moves."

    # 4. Draw Interface
    draw_interface()
    visualizer.draw_maze()

    # 5. Show AI Search Animation
    if solving:
        visible_explored = explored[:min(animation_step, len(explored))]
        path_count = max(0, animation_step - len(explored))
        visible_path = path[:path_count]
    else:
        visible_explored = explored
        visible_path = path

    # Draw Explored Cells
    for x, y in visible_explored:
        pygame.draw.rect(
            screen,
            (65, 135, 210),
            (x * Cell_size, y * Cell_size, Cell_size, Cell_size)
        )

    # Draw Solution Path
    for x, y in visible_path:
        pygame.draw.rect(
            screen,
            (255, 200, 65),
            (x * Cell_size, y * Cell_size, Cell_size, Cell_size)
        )

    # 6. Draw Start and Goal
    visualizer.draw_start()
    visualizer.draw_goal()

    # 7. Draw Human Player
    if mode == "Human":
        x, y = player
        pygame.draw.circle(
            screen,
            (175, 105, 245),
            (
                x * Cell_size + Cell_size // 2,
                y * Cell_size + Cell_size // 2
            ),
            7
        )

    # 8. Display Human Time
    if mode == "Human":
        timer_font = pygame.font.SysFont("Arial", 18)
        timer_text = timer_font.render(
            f"Human Time: {display_time:.2f}s",
            True,
            (255, 255, 255)
        )
        screen.blit(timer_text, (650, 625))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


