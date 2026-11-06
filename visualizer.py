import pygame as py

class MazeVisualizer:
    def __init__(self,screen, maze, start, goal):
        self.screen = screen
        self.maze = maze
        self.start = start
        self.goal = goal

        self.cell_size = 20
        self.wall_color = (0, 0, 0)  # Black
        self.path_color = (255, 255, 255)  # White
        self.start_color = (0, 255, 0)  # Green
        self.goal_color = (255, 0, 0)  # Red

        self.rows=len(maze)
        self.cols=len(maze[0])

        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size


        py.display.set_caption("Smart Maze Solver")

        self.clock = py.time.Clock()

    def draw_maze(self):
        for y in range(self.rows):
            for x in range(self.cols):
                color = self.wall_color if self.maze[y][x] == 1 else self.path_color
                py.draw.rect(
                    self.screen,
                    color,
                    (x * self.cell_size, y * self.cell_size,
                    self.cell_size, self.cell_size),
                )
    def draw_start(self):
        x, y = self.start
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        points = [
            (center_x, center_y - 10),
            (center_x - 10, center_y + 10),
            (center_x + 10, center_y + 10),
        ]
        py.draw.polygon(self.screen, self.start_color, points)
    def draw_goal(self):
        x, y = self.goal
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        py.draw.circle(self.screen, self.goal_color, (center_x, center_y), 10)

    def run(self):
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False

            self.draw_maze()
            self.draw_start()
            self.draw_goal()
            py.display.flip()
            self.clock.tick(60)

        py.quit()