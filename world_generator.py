import random

# Define terrain types
terrain_types = {
    "WALL": "W",
    "DIRT": "D",
    "ROAD": "R",
    "TREE": "T"
}

# World settings
grid_size = 60  # Size of the grid (e.g., 60x60)
world = [[terrain_types["DIRT"] for _ in range(grid_size)] for _ in range(grid_size)]

# Define the size of the wall rectangle in the center
wall_width = 20
wall_height = 10

# Calculate the top-left corner of the wall rectangle
start_x = (grid_size - wall_width) // 2
start_y = (grid_size - wall_height) // 2

# Create the walls
for y in range(start_y, start_y + wall_height):
    for x in range(start_x, start_x + wall_width):
        world[y][x] = terrain_types["WALL"]

# Create a road leading to the center of the wall
road_start_x = 0
road_end_x = start_x + wall_width // 2
road_y = grid_size // 2

for x in range(road_start_x, road_end_x + 1):
    world[road_y][x] = terrain_types["ROAD"]

# Save world to a text file
filename = "world_60x60.txt"
with open(filename, 'w') as file:
    file.write(f"{grid_size}\n")  # First line is the grid size
    for row in world:
        file.write(''.join(row) + "\n")

print(f"World generated and saved to {filename}")
