class Snake:
    def __init__(self):
        self.body = [[5, 5]]  # Starting position (grid coordinates)
        self.direction = 'RIGHT'

    def move(self):
        head = self.body[0]
        if self.direction == 'UP':
            new_head = [head[0], head[1] - 1]
        elif self.direction == 'DOWN':
            new_head = [head[0], head[1] + 1]
        elif self.direction == 'LEFT':
            new_head = [head[0] - 1, head[1]]
        else:
            new_head = [head[0] + 1, head[1]]
        self.body.insert(0, new_head)  # Add new head
        self.body.pop()  # Remove tail unless eating

    def grow(self):
        self.body.append(self.body[-1])  # Add a segment at the tail

    def is_collision(self, screen_width, screen_height, cell_size, walls):
        # Check if snake hits itself or boundaries
        head = self.body[0]
        return (
                head in self.body[1:-1] or  # Exclude the tail from the collision check
                head[0] < 0 or head[1] < 0 or
                head[0] >= screen_width // cell_size or
                head[1] >= screen_height // cell_size
                or head in walls.positions
        )

