import random


class maze_Generator:
    def __init__(self, difficulty="easy", width=None, height=None):
        if width is not None or height is not None:
            self.width = width if width is not None else 21
            self.height = height if height is not None else self.width
        else:
            self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        difficulty = (difficulty or "easy").lower()

        if difficulty == "easy":
            self.width = 21
            self.height = 21
        elif difficulty == "medium":
            self.width = 31
            self.height = 21
        elif difficulty == "hard":
            self.width = 41
            self.height = 31
        else:
            self.width = 21
            self.height = 21

    def generate(self):
        # 1 for wall, 0 for path
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        start = (1, 1)
        goal = (self.width - 2, self.height - 2)

        maze[start[1]][start[0]] = 0
        stack = [start]
        directions = [
            (0, 2), #Down
            (0, -2), #Up
            (2, 0), #Right
            (-2, 0), #Left
        ]

        while stack:
            x, y = stack[-1]
            neighbors = []

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and maze[ny][nx] == 1:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[ny][nx] = 0
                maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        return maze, start, goal