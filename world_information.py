import pygame
from simple_pathfinding import terrain_colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)
BROWN = (139, 69, 19)

class Cell:
    def __init__(self, coordX, coordY, terrain_type):
        self.coordX = coordX
        self.coordY = coordY
        self.terrain_type = terrain_type

    def __eq__(self, other):
        """Equality comparison based on coordinates."""
        if isinstance(other, Cell):
            return self.coordX == other.coordX and self.coordY == other.coordY
        return False

    def __lt__(self, other):
        """Less than comparison, which can be used for sorting or in priority queues."""
        if isinstance(other, Cell):
            return (self.coordX, self.coordY) < (other.coordX, other.coordY)
        return False

    def __hash__(self):
        """Allows the Cell to be used in sets or as keys in dictionaries."""
        return hash((self.coordX, self.coordY))

    def __repr__(self):
        """Readable representation for debugging."""
        return f"Cell({self.coordX}, {self.coordY}, {self.terrain_type})"

    def draw(self, screen, cell_size):
        color = terrain_colors[self.terrain_type]
        rect = pygame.Rect(self.coordX * cell_size, self.coordY * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)


class Pawn:
    def __init__(self, currentPosition: Cell):
        self.currentPostion = currentPosition

    def move(self, direction):
        self.currentPostion.coordX += direction[0]
        self.currentPostion.coordY += direction[1]
        