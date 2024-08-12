import pygame
import sys
from world_information import *
from pathfinding import a_star_search

# Initialize Pygame
pygame.init()

# Define constants
CELL_SIZE = 30  # Adjusted dynamically based on grid size

# Set up display (initial size, will adjust based on input)
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('A* Pathfinding')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)
BROWN = (139, 69, 19)
YELLOW = (209, 202, 2)
BLUE = (2, 145, 255)

# Terrain color mapping
terrain_colors = {
    "W": GREY,  # WALL
    "D": BROWN, # DIRT
    "R": BLACK, # ROAD
    "T": GREEN  # TREE
}

def load_map():
    """Load map from stdin. The first line is the grid size, and the following lines are the terrain types."""
    input_data = sys.stdin.read().strip().splitlines()

    grid_size = int(input_data[0])
    global CELL_SIZE
    CELL_SIZE = 600 // grid_size  # Adjust cell size based on grid size
    grid = []

    for y in range(grid_size):
        row = []
        for x, terrain_type in enumerate(input_data[y + 1]):
            row.append(Cell(x, y, terrain_type.upper()))
        grid.append(row)

    return grid_size, grid

def draw_grid(grid_size):
    for x in range(0, grid_size * CELL_SIZE, CELL_SIZE):
        for y in range(0, grid_size * CELL_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def main():
    heuristic_type = int(sys.argv[1])
    roadBias = sys.argv[2]
    roadBias = True if roadBias == "Y" else False
    
    grid_size, grid = load_map()

    # Adjust screen size based on grid size
    screen = pygame.display.set_mode((grid_size * CELL_SIZE, grid_size * CELL_SIZE))

    start = None
    end = None
    running = True
    path = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                gridX, gridY = mouseX // CELL_SIZE, mouseY // CELL_SIZE

                # Access the correct cell based on the click position
                if 0 <= gridX < grid_size and 0 <= gridY < grid_size:
                    clicked_cell = grid[gridY][gridX]  # Access grid by [row][column] (Y, X)

                    if start is None:
                        start = clicked_cell
                    elif end is None and clicked_cell != start:
                        end = clicked_cell

                    if start is not None and end is not None:
                        path = a_star_search(grid, start, end, roadBias)  # Find path when both start and end are selected

        screen.fill(BLACK)
        draw_grid(grid_size)

        # Draw each cell in the grid with the appropriate color
        for row in grid:
            for cell in row:
                cell.draw(screen, CELL_SIZE)

        # Draw the path
        if (path):
            for cell in path:
                pygame.draw.rect(screen, BLUE, (cell.coordX * CELL_SIZE, cell.coordY * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw start and end points
        if start:
            pygame.draw.rect(screen, RED, (start.coordX * CELL_SIZE, start.coordY * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if end:
            pygame.draw.rect(screen, YELLOW, (end.coordX * CELL_SIZE, end.coordY * CELL_SIZE, CELL_SIZE, CELL_SIZE))


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
