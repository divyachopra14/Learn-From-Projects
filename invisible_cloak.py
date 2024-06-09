# Based on the concept of color detection and segmentation
#importing necessary dependencies

import cv2
import numpy as np
import time

#we can also give a recorded vd rather than recording our own 
cap = cv2.VideoCapture(0)

# give the camera to warm up
time.sleep(2)     
background = 0

# the object cap have a read() function which basically return two values
# one boolean value stating whether it is able to read the frame or not
# and second the frame itself

for i in range(50):
    ret, background = cap.read()

# capturing the background in range of 50
# you should have video that have some seconds
# dedicated to background frame so that it 
# could easily save the background image

# we are reading from video 
while(cap.isOpened()): 
    ret, img = cap.read()
    if not ret:
        break
    # convert the image - BGR to HSV
    # as we focused on detection of red color 
    # converting BGR to HSV for better 
    # detection or you can convert it to gray
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255]) # values is for red colour Cloth
    mask1 = cv2.inRange(hsv, lower_red,upper_red)
    lower_red = np.array([170,120,70])
    upper_red =  np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
    #Combining the masks so that It can be viewd as in one frame
    mask1 = mask1 +mask2
    #After combining the mask we are storing the value in deafult mask.

    #Refining the Mask
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations = 2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations = 1)

    mask2 =cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(background,background,mask=mask1)
    #The basic work of bitwise_and is to combine these background and store it in res1


    res2 = cv2.bitwise_and(img,img,mask=mask2)
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    cv2.imshow('Invisible Cloak',final_output)
    k = cv2.waitKey(10)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()