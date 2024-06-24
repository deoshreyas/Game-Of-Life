import pygame 
from pygame.locals import *
import tomllib
from pathlib import Path

pygame.init()

# SPECIAL PARAMETERS (update for interesting results)
GENERATIONS = "infinite"
FPS = 7
PATTERNS_FILE = Path("patterns.toml")
CELL_SIZE = 10

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)

# WINDOW 
WIDTH, HEIGHT = 500, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game Of Life")

# GRID 
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# LOAD PATTERNS FROM TOML PATTERN FILE
def get_pattern(name, filename=PATTERNS_FILE):
    data = tomllib.loads(filename.read_text(encoding="utf-8"))
    return data[name]["alive_cells"]

# CONSTRUCT GRID FROM PATTERN 
def construct_grid(alive_cells):
    global grid 
    for i in alive_cells:
        if is_valid(i):
            grid[i[0]][i[1]] = 1

# DRAW GRID 
def draw_grid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 1:
                pygame.draw.rect(window, BLACK, rect)
            else:
                pygame.draw.rect(window, LIGHT_GREY, rect, 1)

# CHECK IF A CELL IS VALID (within grid boundaries)
def is_valid(cell):
    return 0 <= cell[0] < GRID_HEIGHT and 0 <= cell[1] < GRID_WIDTH

# CLEAR GRID 
def clear_grid():
    global grid 
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# GET NEIGHBOURS FOR A GIVEN CELL 
def get_neighbours(grid, cell):
    neighbours = 0
    directions = (
            (-1, -1),# Above left
            (-1, 0), # Above
            (-1, 1), # Above right
            (0, -1), # Left
            (0, 1),  # Right
            (1, -1), # Below left
            (1, 0),  # Below
            (1, 1),  # Below right
        )
    for d in directions:
        cellToCheck = (cell[0] + d[0], cell[1] + d[1])
        if is_valid(cellToCheck):
            if grid[cellToCheck[0]][cellToCheck[1]] == 1:
                neighbours += 1
    return neighbours

# LIFE GRID CLASS 
class LifeGrid:
    def __init__(self, grid):
        self.grid = grid 
    
    # evolve the current life grid to the next generation
    def evolve(self):
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                neighbours = get_neighbours(self.grid, (row, col))
                if self.grid[row][col] == 1:
                    # if an alive cell as less than two (underpopulation)
                    # or more than three (overpopulation) neighbours, it dies
                    if neighbours < 2 or neighbours > 3:
                        new_grid[row][col] = 0
                    else:
                        new_grid[row][col] = 1
                else:
                    # if a dead cell has exactly three neighbours, it becomes alive
                    if neighbours == 3:
                        new_grid[row][col] = 1
        return new_grid

# MAIN LOOP 
running = True
clock = pygame.time.Clock()
alive = get_pattern("Blinker")
construct_grid(alive)
patterns = {
    K_1: get_pattern("Blinker"),
    K_2: get_pattern("Toad"),
    K_3: get_pattern("Beacon"),
    K_4: get_pattern("Pulsar"),
    K_5: get_pattern("Penta Decathlon"),
    K_6: get_pattern("Glider"),
    K_7: get_pattern("Glider Gun"),
    K_8: get_pattern("Bunnies"),
    K_9: get_pattern("R-Pentomino"),
    K_0: get_pattern("Puffer-Train")
}
simulating = False
gen = GENERATIONS
life_grid = LifeGrid(grid)
while running:
    clock.tick(FPS) 

    life_grid = LifeGrid(grid)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE: # pause / unpause
                simulating = False if simulating else True
            elif event.key in patterns: # load a pattern
                simulating = False
                clear_grid()
                alive = patterns[event.key]
                construct_grid(alive)
                gen = GENERATIONS
            elif event.key == K_c: # clear the grid 
                simulating = False
                clear_grid()
            elif event.key == K_p: # print alive cells
                simulating = False
                alive_cells = []
                for i in range(GRID_HEIGHT):
                    for j in range(GRID_WIDTH):
                        if grid[i][j] == 1:
                            alive_cells.append([i, j])
                print(alive_cells)
    
    if pygame.mouse.get_pressed()[0] and not simulating:
        x, y = pygame.mouse.get_pos()
        col, row = x // CELL_SIZE, y // CELL_SIZE
        if is_valid((row, col)):
            grid[row][col] = 1
    elif pygame.mouse.get_pressed()[2] and not simulating:
        x, y = pygame.mouse.get_pos()
        col, row = x // CELL_SIZE, y // CELL_SIZE
        if is_valid((row, col)):
            grid[row][col] = 0

    window.fill(WHITE)

    draw_grid(grid)

    if GENERATIONS != "infinite":
        if GENERATIONS > 0 and simulating:
            grid = life_grid.evolve()
            GENERATIONS -= 1
    else:
        if simulating:
            grid = life_grid.evolve()

    pygame.display.update()