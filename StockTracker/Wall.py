import random
import pygame

class Walls:
    def __init__(self):
        self.positions = []  # List of wall positions

    def spawn_wall(self, screen_width, screen_height, cell_size, food, head):
        # Randomly generate a wall position
        x = random.randint(0, screen_width // cell_size - 1)
        y = random.randint(0, screen_height // cell_size - 1)
        if [x, y] not in self.positions and head not in [x, y] and food not in [x, y]:  # Avoid duplicate walls or spawning walls on head or food
            self.positions.append([x, y])

    def draw(self, screen, wall_color, cell_size):
        for wall in self.positions:
            pygame.draw.rect(screen, wall_color, pygame.Rect(wall[0] * cell_size, wall[1] * cell_size, cell_size, cell_size))