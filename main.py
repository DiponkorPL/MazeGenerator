import pygame
from maze import maze_Generator
from visualizer import MazeVisualizer

pygame.init()

generator = maze_Generator(difficulty="medium")

maze, start, goal = generator.generate()

visualizer = MazeVisualizer(generator, maze, start, goal,difficulty="medium")

visualizer.run()

pygame.quit()
