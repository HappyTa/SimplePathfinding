import pygame, constants

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
        """Less than comparison, added so this can be compare in a queue"""
        if isinstance(other, Cell):
            return (self.coordX, self.coordY) < (other.coordX, other.coordY)
        return False

    def __hash__(self):
        """Hasshin capabilities"""
        return hash((self.coordX, self.coordY))

    def __repr__(self):
        return f"Cell({self.coordX}, {self.coordY}, {self.terrain_type})"

    def draw(self, screen, cell_size):
        """Function to draw the cell"""
        color = constants.terrain_colors[self.terrain_type]
        rect = pygame.Rect(self.coordX * cell_size, self.coordY * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)


        """Readable representation for debugging."""

class Pawn:
    def __init__(self, currentPosition: Cell):
        self.currentPostion = currentPosition

    def move(self, direction):
        self.currentPostion.coordX += direction[0]
        self.currentPostion.coordY += direction[1]
        