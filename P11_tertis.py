'''This is the tertis game which is an advanced level Project'''

#importing libraries 
import pygame 
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
s_width = 800 #screen width
s_height = 700 #screen height
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
 
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x # x cordinate
        self.y = y # y cordinate
        self.shape = shape #shape of the block
        self.color = shape_colors[shapes.index(shape)] #color of the block
        self.rotation = 0 #rotation flag
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10) ] for x in range(20)] #BLACK COLOR GRIDS
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)] #locked positions telss if there is any shape block that is occuing any grid blocks
                grid[i][j] = c # if yes the , changing the color of the grid if it is locked
    return grid
 
def convert_shape_format(shape):
    '''
        Most complicated function of the code. This converts the shape dictionary list into actual blocks
    '''
    positions = [] # to get the positions from the shape list where to draw a block 
    format = shape.shape[shape.rotation % len(shape.shape)] # getting the actual list out of shape.shape which is a list of lists

    for i, line in enumerate(format):
        row = list(line) # converting the string in list into a list for easy iteration 
        for j, col in enumerate(row):
            if col ==  '0':
                positions.append((shape.x + j, shape.y + i)) #imagine a graph with x-y axis and shape.x is horizontal values and hence we added j and shape.y is vertical basically row format in grid so add i

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) #offsetting you can skip understanding this line of code

    return positions
 
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0) ] for i in range(20)] # we are onl selecting the black boxes that is empty boxes 
    accepted_pos = [j for sub in accepted_pos for j in sub] #flattening the list -> converted in 1D list
    
    formatted = convert_shape_format(shape)

    for position in formatted:
        if position not in accepted_pos:
            if position[1] > -1: # while the block is falling we need to check if that is in the valid positions, if it's negative it won't be in a valid position so we need greater than it
                return False
    
    return True

def check_lost(positions):
    for pos in positions:
        x,y = pos 
        if y<1:
            return True 
    return False

 
def get_shape():
    global shapes, shape_colors
    return Piece(5,0,random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans",size,bold=True)
    label = font.render(text,1,color)

    surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2), top_left_y +  play_height/2 - (label.get_height()/2)))
    

def draw_grid(surface, grid):
    '''
    This function draws the grid lines 
    '''
    global block_size
    sx = top_left_x #start x
    sy = top_left_y #start y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx,sy+i*block_size), (sx+play_width, sy+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size,sy), (sx+j*block_size, sy+play_height))


def clear_rows(grid, locked):
    '''
    If we make a full row then we need to clear it tha's the only way user can win
    '''
    inc=0
    for i in range(len(grid)-1, -1, -1): #starts from backward 20th row to 0th row
        row = grid[i]
        if (0,0,0) not in row: #no empty squares so completely filled with shapes
            inc += 1 #this tells us how many rows were deleted
            ind = i 
            for j in range(len(row)): #deleting the row
                try:
                    del locked[(j,i)]
                except:
                    continue
            
    #shift every row now 

    if inc > 0:
        for key in sorted(list(locked),key = lambda x: x[1])[::-1]: # reading backward
            x, y = key #getting positions of locked positions
            if y < ind: 
                newKey = (x,y+inc) #tells how many rows to shift 
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    global block_size
    font = pygame.font.SysFont("comicsans",30)
    label = font.render("Next Shape", 1, (255,255,255))

    sx = top_left_x + play_width + 50 #this will give a text in the right empty step
    sy = top_left_y + play_height/2 - 100

    format = shape.shape[shape.rotation]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                pygame.draw.rect(surface, shape.color, (sx+j*block_size, sy+i*block_size , block_size, block_size), 0)

    surface.blit(label,(sx+10,sy-20))
 
def draw_window(surface,grid, score=0, last_score=0):
    global block_size
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont("comicsans",60)
    label = font.render("Tertis",1,(255,255,255))
    surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2), 30)) #to get the middle of thr screen 
    
    #current score
    font = pygame.font.SysFont("comicsans",30)
    label = font.render("Score: "+str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50 #this will give a text in the right empty step
    sy = top_left_y + play_height/2 - 100
    surface.blit(label,(sx+20,sy+160))

    #last max_score
    font = pygame.font.SysFont("comicsans",30)
    label = font.render("High Score: "+str(last_score), 1, (255,255,255))

    sx = top_left_x - 250  #this will give a text in the right empty step
    sy = top_left_y + 100
    surface.blit(label,(sx+20,sy+160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface,grid[i][j],(top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    draw_grid(surface,grid)
    pygame.draw.rect(surface,(255,0,0),(top_left_x,top_left_y,play_width,play_height),5)
    # pygame.display.update()

def update_score(nscore):
    with open('scores.txt','r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    
    with open('scores.txt','w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt','r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score
     
def main(win):
    last_score = max_score()

    locked_positions = {} 
    grid = create_grid(locked_positions) #creating the grid just like we created the board in previous project of connect four

    change_piece = False #change piece flag
    run = True #run flag to run the flag
    current_piece = get_shape() #getting a random shape -> Piece object
    next_piece = get_shape() #getting a random shape -> Piece object
    clock = pygame.time.Clock() #clock objects for defining frames per second to make our game a bit faster
    fall_time = 0 #fall time flag
    fall_speed = 0.27
    level_time = 0 # HOW MUCH TIME HAS PASSES with time the speed of block will increase 
    score = 0

    while run:
        grid = create_grid(locked_positions) #constatntly updating the grid
        fall_time += clock.get_rawtime() #this will tell us how much time the loop took to run 
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1 # this piece of code make the piece move downwards , since the time is is in millisecs so we divide by 1000
            if not(valid_space(current_piece,grid)) and current_piece.y>0:
                current_piece.y -= 1
                change_piece = True #once the moving block has occupied it's position we need to change the piece or shape falling

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if you press the cross button then it will quit the game
                run=False
                pygame.display.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.x += 1 #if it's not a valid space stay on the same place
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.x -= 1 #if it's not a valid space stay on the same place
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.y -= 1 #if it's not a valid space stay on the same place
                elif event.key == pygame.K_UP: #for changing the rotation of the shape
                    current_piece.rotation = current_piece.rotation+1 % len(current_piece.shape)
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation - current_piece.rotation-1 % len(current_piece.shape)
        
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1 : # we are not above the screen while drawing as it will look weird it's just a ui experimented condition remove it and see the difference
                grid[y][x] = current_piece.color #providing the color for the shape

        if change_piece:
            for pos in shape_pos:
                p = (pos[0],pos[1])
                locked_positions[p] = current_piece.color #it is a dictionary with a tuple as key containing x-y cordinates and color as value
            current_piece = next_piece
            next_piece = get_shape()

            change_piece = False

            rows_cleared = clear_rows(grid,locked_positions) # we are calling this function here because while falling down there might be a case when we get a full row but we don't need that
            #this can clear more than 1 rows 
            score += rows_cleared*10

        
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
            draw_text_middle("You lost", 80, (255,255,255),win)
            pygame.display.update()
            pygame.time.delay(2000)
            
            update_score(score)
    
    
def main_menu(win):
    run = True 
    while run:
        win.fill((0,0,0))
        draw_text_middle("Press any key to play", 60, (255,255,255),win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            
            if event.type == pygame.KEYDOWN:
                main(win)
        
    pygame.quit()
    

win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption('Tetris')

main_menu(win)  # start game
