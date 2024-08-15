import heapq, math, constants

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
    # Initialized
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    # Both g and f will be fill with -inf at the start and given a new number as we go
    # g's 1st value will be 0 and f first value will be the distance from it to the goal
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start] = heuristic(start, goal, heuristicType, hWeight)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        # comparing current node with its neighbors
        for direction in DIRECTIONS:
            neighbor_x = current.coordX + direction[0]
            neighbor_y = current.coordY + direction[1]
            
            # Making sure that we are not checking outside the game borders
            if 0 <= neighbor_x < len(grid) and 0 <= neighbor_y < len(grid):
                neighbor = grid[neighbor_y][neighbor_x]

                if neighbor.terrain_type == "W":
                    continue  # Skip walls

                if roadBias == True:
                    tentative_g_score = g_score[current] + terrain_costs[neighbor.terrain_type]
                else:
                    tentative_g_score = g_score[current] + 1

                # If the currnet score is better than said neighbor
                #   Generate new heuristic and update g_score for said neighbor and add it to the queue
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    h = heuristic(neighbor, goal, heuristicType, hWeight)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + h
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