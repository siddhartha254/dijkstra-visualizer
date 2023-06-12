import pygame
from queue import PriorityQueue

WIDTH = 600
SCREEN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Shortest Path Finder using Dijkstra's Algorithm")

# Define colors
RED = (255, 0, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255); YELLOW = (255, 255, 0); TURQUOISE = (64, 224, 208)
WHITE = (255, 255, 255); BLACK = (0, 0, 0); PURPLE = (128, 0, 128); ORANGE = (255, 165, 0); GREY = (128, 128, 128)



def dijkstra(draw, grid, start, end):
    visited = {node: False for row in grid for node in row}
    distance = {node: float("inf") for row in grid for node in row}
    distance[start] = 0
    came_from = {}
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = priority_queue.get()[1]

        if visited[current]:
            continue
        visited[current] = True
        if current == end:
            reconstruct_path(came_from, end, draw)
            return True
        if current != start:
            current.make_closed()
        for neighbor in current.neighbors:
            weight = 1
            if distance[current] + weight < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = distance[current] + weight
                priority_queue.put((distance[neighbor], neighbor))
            if neighbor != end and neighbor != start and not visited[neighbor]:
                neighbor.make_open()
        draw()
    return False


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    #drawing rectangles
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


    def update_neighbors(self, grid):
        self.neighbors = []
        
        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  
            self.neighbors.append(grid[self.row + 1][self.col])

        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  
            self.neighbors.append(grid[self.row - 1][self.col])

        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col + 1])

        #LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

#creates 2D grid of node objects
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

#draws grid lines
def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


#constructs the found path, starts from end node then checks its parent(in came_from) for each and visits that.
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#to draw the grid
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid_lines(win, rows, width)
    pygame.display.update()


#takes mouse position (pos) as parameter
def get_clicked_position(pos, rows, width):
    gap = width // rows
    i, j = pos

    row = i // gap
    col = j // gap
    return row, col


def main(win, width):
    ROWS = 35
    grid = make_grid(ROWS, width)

    start = None; end = None

    run = True; started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]

                if start is None and node != end:
                    start = node
                    start.make_start() #updating color;

                elif end is None and node != start:
                    end = node
                    end.make_end() #updating color;

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN: #for key press;
                if event.key == pygame.K_SPACE and (start) and (end):
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_f:
                    start = None; end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main(SCREEN, WIDTH)