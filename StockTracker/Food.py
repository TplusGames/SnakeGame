import random

class Food:
    def random_position(self, screen_width, screen_height, cell_size, walls):
        x = random.randint(0, screen_width // cell_size - 1)
        y = random.randint(0, screen_height // cell_size - 1)

        if [x, y] not in walls.positions:
            return [x, y]
