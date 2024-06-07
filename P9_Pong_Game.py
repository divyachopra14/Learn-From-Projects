'''
This is a simple Pong game made using Turtle library(which need not be installed).

Step1 import the turtle library
Step2 Create windows screen and set its attributes
Step3 Write the mainloop with the update instruction
Step4 Now we need paddles and the ball make them and set their attributes
Step5 Now that we have paddles we need some movement of paddels, for that movement
      we defined few function paddle_a_up, paddle_a_down, paddle_b_up, paddle_b_down
Step6 Now we need to call these functions while interacting with the keyborad so we the 
      keyboard binding
Step7 Now we need ball to move so we did dx and dy. Then in mainloop we set these cordinates
Step8 Now we need to do border checking if the ball hits any of the 4 borders it should reverse the direction.
Step9 We need the ball to be between the paddles for collision to happen b/w the ball and the paddles, so we put a condt for that
Step10 We need a scoring mechanism as well, so we defined the scores for a and b and coded a pen which will update the scores
        So any player scores only when they hit x border that is vertical border so we updated the scores there
Step11 Now we wanted to add a sound to ball when it hits the border or the paddle, I downloaded this bounce.wav and placed that in the same 
       folder we are making this project in. So import os 
       For MacOS:
            os.syatem("afplay bounce.wav&")
       For Linux:
            os.system("aplay bounce.wav&")
       For Windows:
            import winsound
            winsound.PlaySound("bounce.wav",winsound.SND_ASYNC)
'''


# Simple Pong in Python 3 for Beginners 
import turtle 
import os

win = turtle.Screen()
win.title("Pong by DivyaChopra")
win.bgcolor("black")
win.setup(width=800,height=600)

#Basically what this command does is it actually stops the window from updating.
#So we have to manually update it, it speeds up our game quite a bit
win.tracer(0)

#Score 
score_a=0
score_b=0

#Paddle A or racket A
paddle_a = turtle.Turtle()
paddle_a.speed(0) # this is not the speed that paddle moves on the screen,this is the speed of animation
                #this is something we need to do for the turtle module, it sets the speed to the maximum possible speed otherwise it would be slow
paddle_a.shape("square") #by default it is 20x20 pixels
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5,stretch_len=1)
paddle_a.penup() # Turtles by definition, what they do is they draw a line as they're moving, we don't want to draw lines, because thats not what our program does
                 # so we do pen 
paddle_a.goto(-350,0) # setting the coordinates


#Paddle B or racket B
paddle_b = turtle.Turtle()
paddle_b.speed(0) 
paddle_b.shape("square") 
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5,stretch_len=1)
paddle_b.penup() 
paddle_b.goto(350,0) 

#Ball
ball = turtle.Turtle()
ball.speed(0) 
ball.shape("square") 
ball.color("white")
ball.penup() 
ball.goto(0,0)
ball.dx = 2 #change in x cordinate
ball.dy = 2 #change in y cordinate


#Pen or scoring mechanism
pen=turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player A: 0   Player B: 0",align="center",font={"Courier",50,"normal"})


#Functions 
def paddle_a_up():
    y = paddle_a.ycor() #y coordinate
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor() #y coordinate
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor() #y coordinate
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor() #y coordinate
    y -= 20
    paddle_b.sety(y)


#Keyboard binding
win.listen() # allows us to interact with the keyboard
win.onkeypress(paddle_a_up,"w")
win.onkeypress(paddle_a_down,"s")
win.onkeypress(paddle_b_up,"Up")
win.onkeypress(paddle_b_down,"Down") # arrow keys




#Main Game Loop
while True:
    win.update() # this command updates the window everytiime the loop runs
    # Move the ball
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    # border checking what happens when ball hits the border 
    # height of border is 600 so 300, -300 above and under the ball
    # the ball itself is 20*20

    if ball.ycor()>290:
        ball.sety(290)
        ball.dy *= -1 # reversing the direction of the ball
        os.system("afplay bounce.wav&") # so we addded an & at the back because the sound plays everythings stops but we don't need that so we put an &



    if ball.ycor()< -290:
        ball.sety(-290)
        ball.dy *= -1 # reversing the direction of the ball
        os.system("afplay bounce.wav&")
    
    # width was 800 so +400, -400 to right and left
    
    if ball.xcor() > 390:
        ball.goto(0,0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}   Player B: {}".format(score_a,score_b),align="center",font={"Courier",50,"normal"})
        

    
    if ball.xcor() < -390:
        ball.goto(0,0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a,score_b),align="center",font={"Courier",50,"normal"})



    # we need to make the ball move between the paddle, the paddles are placed at 350,0 and -350,0
    # the width of the paddle is 20 pixels

    # Paddle and Ball Collision
    if (ball.xcor()>340 and ball.xcor()<350) and (ball.ycor()<paddle_b.ycor() + 40 and ball.ycor()>paddle_b.ycor()-40):
        ball.setx(340)
        ball.dx *= -1
        os.system("afplay bounce.wav&")

    if (ball.xcor()< -340 and ball.xcor()> -350) and (ball.ycor()<paddle_a.ycor() + 40 and ball.ycor()>paddle_a.ycor()-40):
        ball.setx(-340)
        ball.dx *= -1
        os.system("afplay bounce.wav&")

    
    
    

    
    


    