import pygame
import random
import subprocess

#Base functions: create_map(x), check_neighbours, refresh_map, print_map(x), draw_map(x)

def create_map(rows, cols):

    map = []
    for y in range(rows):
        row = []
        for x in range(cols):
            row.append(0)

        map.append(row)

    return map


def print_map(map):

    for y in range(len(map)):

        for x in range(len(map[y])):
            print(map[y][x], end='')

        print()

def draw_map(map, background_color, cell_color, rows, cols):
    screen.fill(background_color)
    
    for y in range(len(map)):

        for x in range(len(map[y])):

            if map[y][x] != 0:
                pygame.draw.rect(screen, cell_color, (x * (screen.get_width() / cols), y * (screen.get_height() / rows), screen.get_width() / cols, screen.get_height() / rows))



def check_neighbours(map, rows, cols):
    current_map = create_map(rows+1, cols+1)
    for y in range(len(map)):
        live_cells = 0

        for x in range(len(map[y])):

            #Counting how many live cells are around the current cell
            if y > 0 and x > 0 and x < cols and y < rows:

                live_cells = map[y-1][x-1] + map[y-1][x] + map[y-1][x+1] + map[y][x-1] + map[y][x+1] + map[y+1][x-1] + map[y+1][x] + map[y+1][x+1]

            elif y == 0 and x == 0:
                live_cells = map[y][x] + map[y][x+1] + map[y+1][x] + map[y+1][x+1]

            elif y == cols and x == rows:
                live_cells = map[y-1][x-1] + map[y-1][x] + map[y][x-1] + map[y][x]

            elif y == 0 and x == cols:
                live_cells = map[y][x-1] + map[y][x] + map[y][x] + map[y][x-1] + map[y][x] + map[y+1][x-1] + map[y][x] + map[y+1][x]
            
            elif x == 0 and y == rows:
                live_cells = map[y-1][x] + map[y-1][x] + map[y-1][x+1] + map[y][x-1] + map[y][x+1] + map[y][x-1] + map[y][x] + map[y][x+1]

            elif y == 0 and x > 0 and x < cols:
                live_cells = map[y][x-1] + map[y][x] + map[y][x+1] + map[y][x-1] + map[y][x+1] + map[y+1][x-1] + map[y+1][x] + map[y+1][x+1]

            elif x == 0 and y > 0 and y < rows:
                live_cells = map[y-1][x] + map[y-1][x] + map[y-1][x+1] + map[y][x-1] + map[y][x+1] + map[y+1][x-1] + map[y+1][x] + map[y+1][x+1]

            elif y > 0 and y < rows and x == cols:
                live_cells = map[y-1][x-1] + map[y-1][x] + map[y-1][x] + map[y][x-1] + map[y][x] + map[y+1][x-1] + map[y+1][x] + map[y+1][x]

            elif x > 0 and x < cols and y == rows:
                live_cells = map[y-1][x-1] + map[y-1][x] + map[y-1][x+1] + map[y][x-1] + map[y][x+1] + map[y][x-1] + map[y][x] + map[y][x+1]

            else:
                print("Error: Cell not located")


            live_cells = int(live_cells)


            #Determining if they live or die
            if live_cells < 2 or live_cells > 3:
                current_map[y][x] = 0

            elif live_cells == 3:
                current_map[y][x] = 1

            elif live_cells == 2:
                if map[y][x] == 1:
                    current_map[y][x] = 1
                else:
                    current_map[y][x] = 0 

    return current_map





rows = 100
cols = 100
background_color = (255, 241, 222)
cell_color = (111, 200, 247)
speed = int(input("Enter speed (fps): "))


current_map = []
user = input("Enter your map [none = 100x100 random map]: ")

if user == "":
    map = create_map(rows, cols)
    for y in range(len(map)):
        for x in range(len(map[y])):
            map[y][x] = random.randint(0, 1)
else:
    map = user
    rows = len(map)
    cols = len(map[0])



pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            subprocess.run("pkill -f main.py", shell=True)
            exit()

    current_map = check_neighbours(map, rows-1, cols-1)
    draw_map(current_map, background_color, cell_color, rows, cols)

    if current_map == map:
        print("The map has stabilized.")
        out = input("Close the program? [Y/n]: ")
        exit()

    map = current_map


    
    pygame.display.flip()

    clock.tick(speed)
