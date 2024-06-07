''' 
This is the classic snake game that we used to play in our childhood.
'''

#importing necessary libraries
import tkinter as tk
from tkinter import messagebox
import pygame
import random
from tkinter import messagebox



class cube(object):
    
    '''
    This is a cube class that creates a cube in the grid.
        It has two class attributes rows and w i.e width of the screen 
    '''
    
    
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        '''
            The init function insantiates the object with :
            1. position for eg. like (10,10) now here these are not x y coordinated but we are referring to the 10,10 th 
                cube because our screen is 500 width on that 10,10 will be a small pixel.
            2. direction_x and direction_y we kept dirnx = 1 and dirny = 0 because we wanted our cube to initially move in x direction 
            3. color : color of the cube 
        '''
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
    
    def move(self, dirnx, dirny):
        '''
            the move function of the just changes the location of our cube and updates the necessary attributes
        '''
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        '''
            The draw function is an important function what it does is :
            1. It has two parameters surface i.e screen to draw on and an optional paramenter eyes that is by default false if we need to draw eyes just
                like in case of snake we can send True to this function
            2. We first find out the distance and then i,j that is the starting position of the cube 
            3. Once we have that we draw a rectangle on the surface with the color of the cube , at poition i*distance+1 , j*distance+1 ; so if your start from 10,10
                then we need to draw rectange at 251,251 (now these are actual x and y coordinates and not cube positions), and the reason we added +1 is to avoid drawing 
                the rectangle line over the grid line because we have grid line at (250,250).
                with dimension(Width,height) = distance-2 since it's a square and (a rectangle with equal dimension is also a square); now the reason we used distnce-2 is
                to fit this colored cube inside the grid block so that grid lines as well as cube both are visible
            4. If you want to draw eyes then there is a bit of maths to locate the eyes and then drawing it using pygame

        '''
        distance = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface,self.color,(i*distance+1, j*distance+1, distance-2, distance-2))

        if eyes:
            centre = distance//2
            radius = 3
            circleMiddle = (i*distance+centre-radius, j*distance+8)
            circleMiddle2 = (i*distance + distance-radius*2, j*distance+8)
            pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
            pygame.draw.circle(surface,(0,0,0),circleMiddle2,radius)
        

class snake(object):
    '''
         This is snake class that will include all the methods need to make our snake functional 
         it has two class variables as well body and turns , bosy will keep track of location of cubes with which snake is made up and turns will keep a track where the snake take a turn
    '''
    body = []
    turns = {}
    def __init__(self, color, pos):
        '''
            The init function insantiates the object with :
            1. color : color of the snake 
            2. head : we create head of the snake by creating a cube object and appending in body list as the first cube in the body will be the head
            3. direction_x and direction_y in which the snake is gonna move
        '''
        self.color=color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0 # direction x these are basically flags indicating which direction the snake is moving
        self.dirny = 1 # direction y 

    def move(self):
        '''
            This is the most difficult part of the code, detemining how the snake will move:
            1. We loop through events queue and check if user quits then the game should close. Then we get a list of all keys that can be pressed
               Then we loop through keys and perform the respective actions for eg. if Left key is pressed we update direction x =-1 and direction y = 0 then we then add position of snake's 
               head (which is a cube object) in "turns" dictionary with heads position as key and the new directions as the logic and same logic for other keys as well. The turns dictionary after update looks
               like this {(10, 10): [-1, 0]}
            2. In the second loop we enumerate through body list that is we fetch the indices (denoted by i) and body part (denoted by c) from body list and p is the position of the body part
                The lines of code is explained below . 

        '''
        
        for event in pygame.event.get():  #function is used to retrieve all the events that have occurred since the last time this function was called.events such as mouse clicks, keyboard presses, and other interactions.
            if event.type == pygame.QUIT: # when user closes the window that event is QUIT
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1 # negative direction
                    self.dirny = 0 # not moving in y direction so 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have created a dictionary here and added a key which is the the current position of head of the snake , we are assing the direction in which it turns 
                
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1 # positive x direction
                    self.dirny = 0 # not moving in y direction so 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have created a dictionary here and added a key which is the the current position of head of the snake , we are assing the direction in which it turns 
                
                elif keys[pygame.K_UP]:
                    self.dirnx = 0 # not moving in x direction
                    self.dirny = -1 # in pygame the y coordinate works inversely the more you add the more down it goes so for up we need -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have created a dictionary here and added a key which is the the current position of head of the snake , we are assing the direction in which it turns 
                
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0 # not moving in x direction
                    self.dirny = 1 # in pygame the y coordinate works inversely the more you add the more down it goes so for up we need -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have created a dictionary here and added a key which is the the current position of head of the snake , we are assing the direction in which it turns 
                
        for i, c in enumerate(self.body):
            
            p = c.pos[:] # this [:] This line creates a copy of the current position of the snake segment c
            if p in self.turns: # This checks if the current position p of the snake segment is present in the dictionary self.turns.
                turn = self.turns[p] # f the current position p is found in self.turns, this line retrieves the direction of the turn from the dictionary.
                c.move(turn[0],turn[1]) #This line moves the snake segment c according to the direction specified in turn
                if i == len(self.body)-1: #This condition checks if the current segment being processed is the last segment of the snake's body.
                    self.turns.pop(p) # If the current segment is the last one, it removes the position p from the self.turns dictionary. This indicates that the turn has been processed and the snake can continue moving straight until it reaches the next turn point.
            
            #edge checking
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1]) # if we are going left and hit the edge then go to right
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos=[0,c.pos[1]] # # if we are going right and hit the edge then go to left
                elif c.dirnx == 1 and c.pos[1] >= c.rows-1: c.pos=[c.pos[0],0] # if we going down and hit the edge then go back to top
                elif c.dirnx == -1 and c.pos[1] <= 0: c.pos=[c.pos[0],c.rows-1] # if we going up and hit the edge then go back to bottom
                else: c.move(c.dirnx,c.dirny) # else just move with these coordinates



    def reset(self,pos):
        '''
            This function resets the snake position when it runs into itself.
        '''
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        '''
            This method adds a cube to the snake body when it eats any snack, and extends the body
            1. first we take tail and its directions 
            2. then we check the directions and accordinly place the cube in snake's body
            3. We then sets the directions of new bosy part same as that of the tail
        '''
        
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]))) # If the tail is moving right (dx == 1 and dy == 0), a new segment is added to the left of the tail.
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]))) # If the tail is moving left (dx == -1 and dy == 0), a new segment is added to the right of the tail.
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1))) #If the tail is moving down (dx == 0 and dy == 1), a new segment is added above the tail.
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1))) # If the tail is moving up (dx == 0 and dy == -1), a new segment is added below the tail.

        #These lines set the direction of the newly appended segment to be the same as the direction of the tail.
        self.body[-1].dirnx = dx 
        self.body[-1].dirny = dy

        

    def draw(self,surface):
        '''
            This draws the snake if it is first time we are calling this method it will create a head with eyes, 
            else it will simple draw a cube. This method utilises the cube object and calls the draw menthod of cube class
        '''
        for i, c in enumerate(self.body):
            if i==0:
                c.draw(surface,True) # since this is the first time we are creating the snake we need eyes on his head so that is why this little condition checking
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    '''
        This function draws the grid lines on the surface/screen. 
    '''
    
    sizeBtwn = w // rows # deriving the size of side of the square in grid
    x=0
    y=0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w)) # drawing line on surface of white color at x,0 and x,w ;   Iteration 1. will draw a line at 25,0 and 25,500  Iteration 2 will draw line at 50,0 and 50,500 ... so on and so forth. this line of code draws vertical Lines
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y)) # drawing line on surface of white color at 0,y and w,y ;   Iteration 1. will draw a line at 0,25 and 500,25  Iteration 2 will draw line at 0,50 and 500,50 ... so on and so forth. this line of code draws horizontal lines.  



def redrawWindow(surface):
    '''
        This function redraws the window at each iteration of mainloop
    '''
    global width, rows, s, snack
    surface.fill((0,0,0)) # giving surface a color i.e black
    s.draw(surface) #drawing the snake
    snack.draw(surface) # drawing the snack 
    drawGrid(width,rows,surface) 
    pygame.display.update() # displaying the updated grid

def randomSnack(rows, item):
    '''
       This draws the snack for the snake.
       There are 2 parameters rows and item (which is a snake object) 
       This method return x,y for the snack object
    '''
    positions = item.body # getting the body list from snake object
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        #This line checks if the generated position (x, y) already exists in the list of positions occupied by the snake's body.
        #filter(lambda .pos == (x,y), positions): This creates a filtered list containing only the elements in positions where the position is equal to (x,y)
        # If the generated position is already occupied, the loop continues, generating a new random position.
        # If the generated position is not occupied, the loop breaks, and the function returns the coordinates (x, y).
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0 :
            continue
        else:
            break
    
    return (x,y)

def message_box(subject,content):
    '''
        This functions shows a message when snake runs into itself
    '''
    root=tk.Tk()
    root.attributs("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def main():
    '''
        This is the mainloop. It defines the width, number of rows.
        1. We the create a square display of 500*500
        2. We create a snake and snack object and a flag = True to run the mainloop.
        3. In while loop we start moving the snake and there are two conditions:
            i) if snake eats a snack then we need to add a cube in snake's body
            ii) if snake runs into itself then we need to end the game and show the message and rerun the while loop.
    '''
    
    global width, rows, s, snack # the height variable is not necessary while drawing the squares of the grid 
    width = 500
    height = 500
    rows = 20 #evenly divide the 500*500
    win=pygame.display.set_mode((width,height)) #setting up the screen
    s = snake((255,0,0),(10,10)) # making the snake object with red color and placing it at 10,10 cordinates
    snack = cube(randomSnack(rows,s), color=(0,255,0))
    flag = True 
    
    clock = pygame.time.Clock() #this object makes sure that our snake runs 10 frames one second as we don't want it to move that fast
    
    while flag:
        pygame.time.delay(50) # this helps that our games doesn't move too fast, so a delay of 50 milliseconds, so lower the seconds faster the game
        clock.tick(10) # lower this clock slower the snake
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda x:x.pos, s.body[x+1:])):
                print("Score: " , len(s.body))
                message_box("You Lost","Play Again")
                s.reset((10,10))
                break
        redrawWindow(win)
        

main()