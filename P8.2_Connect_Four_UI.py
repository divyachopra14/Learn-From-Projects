'''
    This is Connect Four game->user interface version. Code is explained line by line below
'''
#importing the libraries
import numpy as np 
import pygame
import sys
import math

#global variables 
BLUE = (0,0,255)
BLACK =(0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    '''
        We create a numpy matrix filled with zeroes and return it.
    '''
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    '''
        We drop a piece at row,col index and assigns it a value same as piece
    '''
    board[row][col] = piece

def is_valid_location(board, col):
    '''
        If the top row of matrix is empty it means we can drop a piece in the matrix. We are using 5th row because we are printing flipped board later.
    '''
    return board[5][col] == 0


def get_next_open_row(board, col):
    '''
        This method is to get the next available or empty row.
    '''
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def draw_board(board):
    '''
         This function draws the board. 
         
         The first for loop creates the blue rectangles and black circles in it. c*SQUARESIZE gives the x coordinate like for c=1 1*100 = 100,
         r*SQUARESIZE+SQUARESIZE gives the y coordinate skipping the first row as that we need for diaplaying the message , 1*100+100=200 so (100,200), (100,300), 
         (100,400)...son on and so forth.

         The second loop updates the board if any ball is dropped uding the board matrix (a numpy matrix)
    '''
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), int(RADIUS))
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), int(RADIUS))
            elif board[r][c]==2:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), int(RADIUS))
    pygame.display.update()

def winning_move(board, piece):
    '''
        This functions checks if any player connect four cosecutive locations by iterating over every possible combination.
    '''
    # Check all the horizontal locations for win
    for c in range(COLUMN_COUNT - (COLUMN_COUNT%4)):
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    
    # Check all the vertical locations for win 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (ROW_COUNT%4)):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    
    # Check for positively sloped diagonals 
    for c in range(COLUMN_COUNT- (COLUMN_COUNT%4)):
        for r in range(ROW_COUNT - (ROW_COUNT%4)):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True

    # Check for negatively sloped diagonals
    for c in range(COLUMN_COUNT - (COLUMN_COUNT%4)):
        for r in range((ROW_COUNT%4),ROW_COUNT):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True

def print_board(board):
    '''
         This function flips the board and prints it. If we don't flip it then it will drop the ball in first row instead of last so we print inverted matrix to see the desired results.
    '''
    print(np.flip(board,0))


board = create_board()
game_over = False
turn = 0 

pygame.init()

SQUARESIZE = 100 #(in pixels)

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width,height)

RADIUS = int(SQUARESIZE/2 - 5) # we need a circle smaller than rectangle so that it can fit in that's why we do -5

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace",75)

#main_loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # this line prevents drawing circle on every motion of the mouse
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)),RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)),RADIUS)
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE)) # to prevent continuous chain of circles on scrolling 
            if turn == 0:
                posx = event.pos[0] # this give the position where we click our mouse
                col = int(math.floor(posx/SQUARESIZE)) # to get a range between 1-7 just like we had 0-6
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,1)

                    if winning_move(board, 1):

                        label = myfont.render("Player 1 wins!!",1, RED)
                        screen.blit(label,(40,10)) # updates the specific part of the screen
                        game_over=True
            # # Ask for Player1 Input 
            else:
                posx = event.pos[0] # this give the position where we click our mouse
                col = int(math.floor(posx/SQUARESIZE)) # to get a range between 1-7 just like we had 0-6
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!",1, YELLOW)
                        screen.blit(label,(40,10))
                        game_over=True
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)