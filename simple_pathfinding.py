import pygame
import sys
from world_information import *
from pathfinding import * 


# Initialize Pygame
pygame.init()

# Define constants
CELL_SIZE = 30  # Adjusted dynamically based on grid size
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10

# Define colors
BLACK = (45,45,45)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)
BROWN = (101, 78, 61)
YELLOW = (209, 202, 2)
BLUE = (2, 145, 255)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Terrain color mapping
terrain_colors = {
    "W": GREY,  # WALL
    "D": BROWN, # DIRT
    "R": BLACK, # ROAD
    "T": GREEN  # TREE
}

# Set up display (initial size, will adjust based on input)
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Simple Pathfinding')

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

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

def reset_grid():
    return None, None, []  # Reset start, end, and path

heuristic_type = None

def main():
    global heuristic_type
    hWeight = float(sys.argv[1])
    roadBias = sys.argv[2]
    heuristic_type = 0 # Default is manhattan
    roadBias = True if roadBias == "Y" else False
    
    grid_size, grid = load_map()

    # Adjust screen size based on grid size
    screen = pygame.display.set_mode((grid_size * CELL_SIZE + BUTTON_WIDTH + BUTTON_MARGIN, grid_size * CELL_SIZE))

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
                        path = a_star_search(grid, start, end, heuristicType=heuristic_type, roadBias=roadBias, hWeight=hWeight)  # Find path when both start and end are selected

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start, end, path = reset_grid()
                        
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

        # Draw buttons for heuristic selection
        draw_button("Manhattan", grid_size * CELL_SIZE + BUTTON_MARGIN, 10, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_heuristic(0) )
        draw_button("Chebyshev", grid_size * CELL_SIZE + BUTTON_MARGIN, BUTTON_HEIGHT + 20, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_heuristic(1))
        draw_button("Euclidean", grid_size * CELL_SIZE + BUTTON_MARGIN, 2 * BUTTON_HEIGHT + 30, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_heuristic(2))



        pygame.display.flip()

    pygame.quit()
    sys.exit()

def set_heuristic(new):
    global heuristic_type
    if heuristic_type != new:
        heuristic_type = new

if __name__ == "__main__":
    main()
