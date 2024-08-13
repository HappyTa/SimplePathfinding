import heapq
import math
from world_information import *

# Directions for 8-way movement
DIRECTIONS = [
    (-1, 0), (1, 0), (0, -1), (0, 1), 
    (-1, -1), (1, 1), (-1, 1), (1, -1)
]

# Terrain movement costs (lower is better)
terrain_costs = {
    "W": float('inf'),  # WALL
    "D": 4,             # DIRT
    "R": 1,             # ROAD
    "T": 3              # TREE
}

def heuristic(a, b, type = 0, weight = 1):
    if type == 0: # Manhattan
        return weight * (abs(a.coordX - b.coordX) + abs(a.coordY - b.coordY))
    elif type == 1: #Chebyshev Distance
        return weight * max(abs(a.coordX - b.coordX),abs(a.coordY - b.coordY))
    else: # Euclidian
        return weight * math.sqrt((a.coordX - b.coordX)**2 + (a.coordY - b.coordY)**2)

def a_star_search(grid, start, goal, heuristicType = 0, roadBias = True, hWeight = 1):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start] = heuristic(start, goal, heuristicType, hWeight)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for direction in DIRECTIONS:
            neighbor_x = current.coordX + direction[0]
            neighbor_y = current.coordY + direction[1]

            if 0 <= neighbor_x < len(grid) and 0 <= neighbor_y < len(grid):
                neighbor = grid[neighbor_y][neighbor_x]

                if neighbor.terrain_type == "W":
                    continue  # Skip walls

                if roadBias == True:
                    tentative_g_score = g_score[current] + terrain_costs[neighbor.terrain_type]
                else:
                    tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    h = heuristic(neighbor, goal, heuristicType, hWeight)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + h + 0.001 * h # f score is bias toward the goal
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return an empty path if there's no path

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
    return path