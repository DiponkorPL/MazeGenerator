
import pygame
import time
from solver import bfs, a_star,solve_best_algorithm


class MazeVisualizer:
    def __init__(self, generator, maze, start, goal,difficulty="medium"):
        self.generator = generator
        self.difficulty = difficulty

        # *Screen Settings
        self.screen_width = 1000
        self.maze_margin = 110
        self.cell_size = 20
        self.fullscreen = False

        # Maze Information
        self.maze = maze
        self.start = start
        self.goal = goal

        self.rows = len(maze)
        self.cols = len(maze[0])

        # *Maze Position
        self.maze_offset_y = self.maze_margin
        
        # *Fixed Cell Size
        self.cell_size = 20
        # Maze Dimensions
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size

        # *Screen Height
        self.bottom_panel_height = 140
        self.screen_height = (
            self.maze_offset_y + self.height + self.bottom_panel_height
        )

        # Window Setup
        self.windowed_size = (max(1000,self.width+40), self.screen_height)
        self.screen = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)
        pygame.display.set_caption("Smart Maze Lab")

        # *Colors
        self.wall_color = (0, 0, 0)
        self.path_color = (255, 255, 255)
        self.start_color = (0, 255, 0)
        self.goal_color = (255, 0, 0)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.timer_font = pygame.font.SysFont("Arial", 18)

        # *Buttons
        self.buttons = {
            "New Maze": pygame.Rect(20, 10, 150, 40),
            "Human": pygame.Rect(190, 10, 150, 40),
            "Solve": pygame.Rect(370, 10, 150, 40),
            "Reset": pygame.Rect(548, 10, 150, 40),
            "Easy": pygame.Rect(20, 60, 120, 35),
            "Medium": pygame.Rect(155, 60, 120, 35),
            "Hard": pygame.Rect(290, 60, 120, 35)
        }

        # *Game Variables
        self.player = start
        self.mode = "Ready"
        self.algorithm = None
        self.status = "Choose Human or AI"

        self.moves = 0

        self.human_start_time = None
        self.human_elapsed_time = 0.0
        self.solver_elapsed_time = 0.0
        self.display_time = 0.0

        self.explored = []
        self.path = []

        self.solving = False
        self.animation_step = 0
        self.animation_counter = 0
        self.animation_delay = 2

    # Toggle Fullscreen
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.windowed_size = self.screen.get_size()
            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                self.windowed_size,
                pygame.RESIZABLE
            )
    # *Reset Game
    def reset_game(self):
        self.player = self.start
        self.mode = "Ready"
        self.algorithm = None
        self.status = "Choose Human or AI"

        self.moves = 0

        self.human_start_time = None
        self.human_elapsed_time = 0.0
        self.solver_elapsed_time = 0.0
        self.display_time = 0.0

        self.explored = []
        self.path = []

        self.solving = False
        self.animation_step = 0
        self.animation_counter = 0

    #* Update Maze Layout
    def update_maze_layout(self):
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.screen_height = (
            self.maze_offset_y
            + self.height
            + self.bottom_panel_height
        )
        self.windowed_size = (
            max(1000, self.width + 40),
            self.screen_height
        )
        if not self.fullscreen:
            self.screen = pygame.display.set_mode(
                self.windowed_size,
                pygame.RESIZABLE
            )

    # *Change Difficulty
    def change_difficulty(self, level):
        self.difficulty = level
        self.generator.set_difficulty(level)
        self.maze, self.start, self.goal = (
            self.generator.generate()
        )
        self.update_maze_layout()

        self.reset_game()

    # Generate New Maze
    def new_maze(self):
        self.maze, self.start, self.goal = (
            self.generator.generate()
        )
        self.update_maze_layout()
        self.reset_game()

    #* Run both algorithms and select the best result
    def solve_maze(self):
        path, explored, elapsed_time, algorithm = solve_best_algorithm(
            self.maze,
            self.start,
            self.goal
        )
        self.path = path
        self.explored = explored
        self.algorithm = algorithm
        self.elapsed_time = elapsed_time
        if not path:
            self.status = "No solution found!"
            self.mode = "Ready"
            return
        # Start AI visualization
        self.mode = "AI"
        self.status = f"{algorithm} selected and solving maze"
        self.animation_step = 0
        self.solving = True

    # *Human Mode
    def start_human_mode(self):
        self.player = self.start
        self.mode = "Human"
        self.algorithm = None
        self.status = "Use Arrow Keys or WASD"

        self.moves = 0

        self.human_start_time = time.perf_counter()
        self.human_elapsed_time = 0.0
        self.solver_elapsed_time = 0.0

        self.explored = []
        self.path = []
        self.solving = False

    # *AI Solver
    def start_ai_solver(self, solver_function, algorithm_name):
        self.mode = "AI"
        self.algorithm = algorithm_name
        self.status = f"Solving with {algorithm_name}..."

        self.player = self.start
        self.moves = 0

        self.path, self.explored, self.solver_elapsed_time = (
            solver_function(self.maze, self.start, self.goal)
        )
        self.animation_step = 0
        self.animation_counter = 0
        self.solving = bool(self.path)
        if not self.path:
            self.status = "No path found by the AI solver."
        else:
            self.status = (
                f"AI solver found a path with "
                f"{len(self.path)} steps."
            )

    # *Human Player Movement
    def move_player(self, dx, dy):
        if self.mode != "Human":
            return

        if self.status == "You reached the goal!":
            return

        x, y = self.player

        nx = x + dx
        ny = y + dy

        if (
            0 <= nx < self.cols
            and 0 <= ny < self.rows
            and self.maze[ny][nx] == 0
        ):
            self.player = (nx, ny)
            self.moves += 1

            if self.player == self.goal:
                self.status = "You reached the goal!"

                if self.human_start_time is not None:
                    self.human_elapsed_time = (
                        time.perf_counter() - self.human_start_time
                    )

    # *Draw Button
    def draw_button(self, text, rect, color):
        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=8
        )
        label = self.font.render(
            text,
            True,
            (255, 255, 255)
        )
        self.screen.blit(
            label,
            label.get_rect(center=rect.center)
        )

    # *Draw Interface
    def draw_interface(self):
        self.screen.fill((18, 22, 32))

        # Draw Buttons at Top
        self.draw_button(
            "New Maze",
            self.buttons["New Maze"],
            (40, 100, 170)
        )
        self.draw_button(
            "Easy",
            self.buttons["Easy"],
            (35, 130, 85) if self.difficulty == "easy"
            else (75, 83, 104)
        )
        self.draw_button(
            "Medium",
            self.buttons["Medium"],
            (35, 130, 85) if self.difficulty == "medium"
            else (75, 83, 104)
        )

        self.draw_button(
            "Hard",
            self.buttons["Hard"],
            (35, 130, 85) if self.difficulty == "hard"
            else (75, 83, 104)
        )
        self.draw_button(
            "Human",
            self.buttons["Human"],
            (35, 130, 85)
        )
        self.draw_button(
            "Solve",
            self.buttons["Solve"],
            (45, 105, 170)
        )
        self.draw_button(
            "Reset",
            self.buttons["Reset"],
            (75, 83, 104)
        )

        #* Game Information Below Maze
        info_y = self.maze_offset_y + self.height + 10

        info = [
            f"Difficulty: {self.difficulty.capitalize()}",
            f"Mode: {self.mode}",
            f"Algorithm: {self.algorithm or 'None'}",
            f"Moves: {self.moves}",
            f"Time: {self.display_time:.2f}s",
            f"Path Length: {max(0, len(self.path) - 1)}",
            f"Explored: {len(self.explored)}"
            f"Algorithm: {self.algorithm or 'None'}"
        ]

        for i, text in enumerate(info):
            label = self.small_font.render(
                text,
                True,
                (255, 255, 255)
            )
            self.screen.blit(
                label,
                (20 + (i % 3) * 250, info_y + (i // 3) * 25)
            )


        # Status

        status_text = self.small_font.render(
            self.status[:80],
            True,
            (100, 220, 160)
        )

        self.screen.blit(
            status_text,
            (20, info_y + 70)
        )

    # *Handle Mouse and Keyboard Events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.windowed_size = event.w, event.h
                    self.screen = pygame.display.set_mode(
                        self.windowed_size,
                        pygame.RESIZABLE
                    )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if self.buttons["Easy"].collidepoint(mouse_pos):
                        self.change_difficulty("easy")
                    elif self.buttons["Medium"].collidepoint(mouse_pos):
                        self.change_difficulty("medium")
                    elif self.buttons["Hard"].collidepoint(mouse_pos):
                        self.change_difficulty("hard")
                    elif self.buttons["New Maze"].collidepoint(mouse_pos):
                        self.new_maze()
                    elif self.buttons["Human"].collidepoint(mouse_pos):
                        self.start_human_mode()
                    elif self.buttons["Solve"].collidepoint(mouse_pos):
                        self.solve_maze()
                    elif self.buttons["Reset"].collidepoint(mouse_pos):
                        self.reset_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.mode == "Human":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.move_player(0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.move_player(0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.move_player(-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.move_player(1, 0)

        return True

    # *Update Timer
    def update_timer(self):
        if self.mode == "Human" and self.human_start_time is not None:
            if self.status == "You reached the goal!":
                self.display_time = self.human_elapsed_time
            else:
                self.display_time = (
                    time.perf_counter() - self.human_start_time
                )
        elif self.mode == "AI":
            self.display_time = self.solver_elapsed_time
        else:
            self.display_time = 0.0

    # *Update AI Animation
    def update_animation(self):
        if self.solving:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delay:
                self.animation_counter = 0
                self.animation_step += 1
                total_steps = len(self.explored) + len(self.path)
                if self.animation_step >= total_steps:
                    self.animation_step = total_steps
                    self.solving = False
                    self.status = (
                        f"{self.algorithm} completed! "
                        f"Shortest path: {len(self.path) - 1} moves."
                    )

    # *Draw Maze
    def draw_maze(self):
        for y in range(self.rows):
            for x in range(self.cols):
                color = (
                    self.wall_color
                    if self.maze[y][x] == 1
                    else self.path_color
                )
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        x * self.cell_size,
                        y * self.cell_size+self.maze_margin,
                        self.cell_size,
                        self.cell_size
                    )
                )

    # *Draw AI Search Animation
    def draw_search_animation(self):
        if self.solving:
            visible_explored = self.explored[
                :min(self.animation_step, len(self.explored))
            ]
            path_count = max(
                0,
                self.animation_step - len(self.explored)
            )
            visible_path = self.path[:path_count]
        else:
            visible_explored = self.explored
            visible_path = self.path

        # *Explored Cells
        for x, y in visible_explored:
            pygame.draw.rect(
                self.screen,
                (65, 135, 210),
                (
                    x * self.cell_size,
                    y * self.cell_size+self.maze_margin,
                    self.cell_size,
                    self.cell_size
                )
            )

        # *Solution Path
        for x, y in visible_path:
            pygame.draw.rect(
                self.screen,
                (255, 200, 65),
                (
                    x * self.cell_size,
                    y * self.cell_size+self.maze_margin,
                    self.cell_size,
                    self.cell_size
                )
            )

    #* Draw Start
    def draw_start(self):
        x, y = self.start
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2+self.maze_margin
        direction = "up"
        if self.mode=="AI" and len(self.path) > 1:
            next_x, next_y = self.path[1]
            dx = next_x - x
            dy = next_y - y
            if dx == 1:
                direction = "right"
            elif dx == -1:
                direction = "left"
            elif dy == 1:
                direction = "down"
            elif dy == -1:
                direction = "up"
        if direction == "up":
            points = [
                (center_x, center_y - 10),
                (center_x - 9, center_y + 8),
                (center_x + 9, center_y + 8)
            ]
        elif direction == "down":
            points = [
                (center_x, center_y + 10),
                (center_x - 9, center_y - 8),
                (center_x + 9, center_y - 8)
            ]
        elif direction == "left":
            points = [
                (center_x - 10, center_y),
                (center_x + 8, center_y - 9),
                (center_x + 8, center_y + 9)
            ]
        elif direction == "right":
            points = [
                (center_x + 10, center_y),
                (center_x - 8, center_y - 9),
                (center_x - 8, center_y + 9)
            ]
        pygame.draw.polygon(
            self.screen,
            self.start_color,
            points
        )
    #* Draw Goal
    def draw_goal(self):
        x, y = self.goal
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2+self.maze_margin

        pygame.draw.circle(
            self.screen,
            self.goal_color,
            (center_x, center_y),
            10
        )

    #* Draw Human Player
    def draw_player(self):
        if self.mode == "Human":
            x, y = self.player

            pygame.draw.circle(
                self.screen,
                (175, 105, 245),
                (
                    x * self.cell_size + self.cell_size // 2,
                    y * self.cell_size + self.cell_size // 2+self.maze_margin
                ),
                7
            )

    #* Draw Timer
    def draw_timer(self):
        if self.mode == "Human":
            timer_text = self.timer_font.render(
                f"Human Time: {self.display_time:.2f}s",
                True,
                (255, 255, 255)
            )
            self.screen.blit(timer_text, (650, 625))

    #* Main Game Loop
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_timer()
            self.update_animation()

            self.draw_interface()
            self.draw_maze()
            self.draw_search_animation()
            self.draw_start()
            self.draw_goal()
            self.draw_player()

            pygame.display.flip()
            self.clock.tick(60)
