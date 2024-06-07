'''
    This is Connect Four game->command line version. Code is explained line by line below
'''
#importing the library
import numpy as np 

#global variables for dimensions of the matrix

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
        
def print_board(board):
    '''
         This function flips the board and prints it.
    '''
    print(np.flip(board,0))

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

game_over = False
board = create_board()
print_board(board)
turn = 0

#main_loop
while not game_over:
    # Ask for Player1 Input 
    if turn == 0:
        col = int(input("Player 1 Make Your Selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board,col)
            drop_piece(board,row,col,1)
            print_board(board)
            if winning_move(board, 1):
                print("Player1 Won!!! Congrats!!!")
                game_over=True
        else:
            print("Choose again!")
            continue
    # Ask for Player1 Input 
    else:
        col = int(input("Player 2 make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board,col)
            drop_piece(board,row,col,2)
            print_board(board)
            if winning_move(board, 2):
                print("Player2 Won!!! Congrats!!!")
                game_over=True
        else:
            print("Choose again! ")
            continue
    turn += 1
    turn = turn % 2