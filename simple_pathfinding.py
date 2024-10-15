import pygame
import sys
import constants
import settings
from world_information import Cell
from pathfinding import a_star_search

# Initialize Pygame
pygame.init()

# Set up display (initial size, will adjust based on input)
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Simple Pathfinding")


def load_map():
    """Load map from stdin. The first line is the grid size, and the following lines are the terrain types."""
    input_data = sys.stdin.read().strip().splitlines()

    grid_size = int(input_data[0])
    # global CELL_SIZE
    constants.CELL_SIZE = 600 // grid_size  # Adjust cell size based on grid size
    grid = []

    for y in range(grid_size):
        row = []
        for x, terrain_type in enumerate(input_data[y + 1]):
            row.append(Cell(x, y, terrain_type.upper()))
        grid.append(row)

    return grid_size, grid


def draw_grid(grid_size):
    for x in range(0, grid_size * constants.CELL_SIZE, constants.CELL_SIZE):
        for y in range(0, grid_size * constants.CELL_SIZE, constants.CELL_SIZE):
            rect = pygame.Rect(x, y, constants.CELL_SIZE, constants.CELL_SIZE)
            pygame.draw.rect(screen, constants.WHITE, rect, 1)


def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            pygame.draw.rect(
                screen, constants.BUTTON_SELECT_COLOR, (x, y, width, height)
            )
            action()
            pygame.time.delay(200)
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, constants.BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


def draw_label(text, x, y):
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, constants.WHITE)
    # global screen
    screen.blit(text_surf, (x, y))


def reset_grid():
    return None, None, []  # Reset start, end, and path


# heuristic_type = None
def main():
    settings.hWeight = float(sys.argv[1])
    grid_size, grid = load_map()

    # Adjust screen size based on grid size
    screen = pygame.display.set_mode(
        (
            grid_size * constants.CELL_SIZE
            + constants.BUTTON_WIDTH
            + constants.BUTTON_MARGIN,
            grid_size * constants.CELL_SIZE,
        )
    )

    start = None
    end = None
    running = True
    path = []

    while running:
        # "Event handler"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                gridX, gridY = (
                    mouseX // constants.CELL_SIZE,
                    mouseY // constants.CELL_SIZE,
                )

                # Making sure that the user is clicking on the map
                if 0 <= gridX < grid_size and 0 <= gridY < grid_size:
                    clicked_cell = grid[gridY][
                        gridX
                    ]  # Access grid by [row][column] (Y, X)

                    if start is None:
                        start = clicked_cell
                    elif end is None and clicked_cell != start:
                        end = clicked_cell

                    # Only do the search if both start and finish is chosen
                    # Need to add functionality that notify the user if the path is impossibble
                    if start is not None and end is not None:
                        path = a_star_search(
                            grid,
                            start,
                            end,
                            heuristicType=settings.heuristic_type,
                            roadBias=settings.road_bias,
                            straightBias=settings.straight_bias,
                            hWeight=settings.hWeight,
                        )  # Find path when both start and end are selected

            # Reset key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start, end, path = reset_grid()

        screen.fill(constants.BLACK)
        draw_grid(grid_size)

        # Color the cells
        for row in grid:
            for cell in row:
                cell.draw(screen, constants.CELL_SIZE)

        # Draw the path
        if path:
            for cell in path:
                pygame.draw.rect(
                    screen,
                    constants.BLUE,
                    (
                        cell.coordX * constants.CELL_SIZE,
                        cell.coordY * constants.CELL_SIZE,
                        constants.CELL_SIZE,
                        constants.CELL_SIZE,
                    ),
                )

        # Draw start and end points
        if start:
            pygame.draw.rect(
                screen,
                constants.RED,
                (
                    start.coordX * constants.CELL_SIZE,
                    start.coordY * constants.CELL_SIZE,
                    constants.CELL_SIZE,
                    constants.CELL_SIZE,
                ),
            )
        if end:
            pygame.draw.rect(
                screen,
                constants.YELLOW,
                (
                    end.coordX * constants.CELL_SIZE,
                    end.coordY * constants.CELL_SIZE,
                    constants.CELL_SIZE,
                    constants.CELL_SIZE,
                ),
            )

        # Draw buttons
        draw_button(
            "Manhattan",
            grid_size * constants.CELL_SIZE + constants.BUTTON_MARGIN - 15,
            10,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            constants.BUTTON_COLOR,
            constants.BUTTON_HOVER_COLOR,
            lambda: set_heuristic(0),
        )
        draw_button(
            "Chebyshev",
            grid_size * constants.CELL_SIZE + constants.BUTTON_MARGIN - 15,
            constants.BUTTON_HEIGHT + 20,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            constants.BUTTON_COLOR,
            constants.BUTTON_HOVER_COLOR,
            lambda: set_heuristic(1),
        )
        draw_button(
            "Euclidean",
            grid_size * constants.CELL_SIZE + constants.BUTTON_MARGIN - 15,
            2 * constants.BUTTON_HEIGHT + 30,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            constants.BUTTON_COLOR,
            constants.BUTTON_HOVER_COLOR,
            lambda: set_heuristic(2),
        )

        draw_button(
            "Road Bias",
            grid_size * constants.CELL_SIZE
            + constants.BUTTON_MARGIN
            - (constants.BUTTON_MARGIN // 2),
            3 * constants.BUTTON_HEIGHT + 40,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            constants.BUTTON_COLOR,
            constants.BUTTON_HOVER_COLOR,
            lambda: set_road_bias(),
        )

        draw_button(
            "Straight Bias",
            grid_size * constants.CELL_SIZE
            + constants.BUTTON_MARGIN
            - (constants.BUTTON_MARGIN // 2),
            4 * constants.BUTTON_HEIGHT + 50,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
            constants.BUTTON_COLOR,
            constants.BUTTON_HOVER_COLOR,
            lambda: set_straight_bias(),
        )

        # Draw current heuristic
        draw_label(
            f"h_type: {settings.heuristic_type}",
            grid_size * constants.CELL_SIZE,
            5 * constants.BUTTON_HEIGHT + 70,
        )
        # Draw labels to display road_bias and straight_bias values
        draw_label(
            f"Road Bias: {'Y' if settings.road_bias else 'N'}",
            grid_size * constants.CELL_SIZE,
            6 * constants.BUTTON_HEIGHT + 80,
        )
        draw_label(
            f"Straight Bias: {'Y' if settings.straight_bias else 'N'}",
            grid_size * constants.CELL_SIZE,
            7 * constants.BUTTON_HEIGHT + 90,
        )

        pygame.display.flip()
    pygame.quit()
    sys.exit()


def set_heuristic(new):
    if settings.heuristic_type != new:
        settings.heuristic_type = new


def set_road_bias():
    settings.road_bias = not settings.road_bias


def set_straight_bias():
    settings.straight_bias = not settings.straight_bias


if __name__ == "__main__":
    main()
