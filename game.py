import os   #access the directives the frames
import random   #to generate random numbers
import time     #time module taking current time
import numpy as np  
import cv2

folderpath='frames'
mylist = os.listdir(folderpath)
graphic=[cv2.imread(f'{folderpath}/{impath}') for impath in mylist]
green=graphic[0];
red=graphic[1];
kill=graphic[2];
winner=graphic[3];
intro=graphic[4];

cv2.imshow('Squid game',cv2.resize(intro,(0,0),fx=0.67,fy=0.67))
cv2.waitKey(1)  #frames dont clash with each other

while True:
    cv2.imshow('Squid game',cv2.resize(intro,(0,0),fx=0.67,fy=0.67))
    if cv2.waitKey(1) & 0xFF==ord('q'):     #after pressing we can exit from the frame user press q the while loop will break
        break

TIMER_MAX = 45        #so that user gets only 45 sec to complete the game
TIMER=TIMER_MAX
maxMove=6500000     #how frequently the red and green will change- if we give 5 then how many times the light will change
font=cv2.FONT_HERSHEY_COMPLEX_SMALL
cap=cv2.VideoCapture(0)     #it captures the video from webcam, if u have exter webcam it will become 1
frameHeight=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  #assigned the webcam and the height
frameWidth=cap.get(cv2.CAP_PROP_FRAME_WIDTH)     #it does the width

win=False   #variable whether the game is won or not in default its false

prev=time.time()    #previous time means prev frame is updated
prevDoll=prev
showFrame=cv2.resize(green,(0,0),fx=0.67,fy=0.67)
isgreen=True        #its tracks wherther the light is green or not

while cap.isOpened() and TIMER>=0:      #cap is video stream is running and then timer is 0 then time is checked and if its greather then its light is green or not and if red then then stop and if red light is there and pressed 'w' then its over
    if isgreen and(cv2.waitKey(10) & 0xFF==ord('w')):
        win=True        #then it determine that user is win or not
        break

    ret,frame=cap.read()        #from cap the frame is read one by one

    cv2.putText(showFrame,str(TIMER),
                (67,67),font,1,(0,int(255*(TIMER)/TIMER_MAX),int(255*(TIMER_MAX-TIMER)/TIMER_MAX)),4,cv2.LINE_AA)
    

    cur=time.time()

    no=random.randint(1,5)
    if cur-prev>=no:
        prev=cur    #current time
        TIMER=TIMER-no
        if cv2.waitKey(10) & 0xFF==ord('w'):
            win=True
            break

        if isgreen:
            showFrame=cv2.resize(red,(0,0),fx=0.67,fy=0.67)
            isgreen=False
            ref=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)      #image is 3 layer rgb, convert into gray

        else:
            showFrame=cv2.resize(green,(0,0),fx=0.67,fy=0.67)
            isgreen=True
    
    if not isgreen:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frameDelta=cv2.absdiff(ref,gray)    #its absolute , frame is changing then numpy is change, and then we find the diff btw the red light and user, if its 0 then no movement, if thats a value we know we have a movement
        thresh=cv2.threshold(frameDelta,20,255,cv2.THRESH_BINARY)[1]        #kitna change hua hai usko wa variable me store kar deta hu
        change=np.sum(thresh)

        if change>maxMove:
            break
    else:
        if cv2.waitKey(10) & 0xFF==ord('w'):
            win=True
            break

    camshow=cv2.resize(frame,(0,0),fx=0.4,fy=0.4)   #we showing the frame through camera

    camH,camW=camshow.shape[0],camshow.shape[1]
    showFrame[0:camH,-camW:]=camshow

    cv2.imshow('Squid game',showFrame)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
cap.release()
if not win:
    for i in range(10):
        cv2.imshow('Squid game',cv2.resize(kill,(0,0),fx=0.67,fy=0.67))

    while True:
        cv2.imshow('Squid game',cv2.resize(kill,(0,0),fx=0.67,fy=0.67))
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break

else:
    cv2.imshow('Squid game',cv2.resize(winner,(0,0),fx=0.67,fy=0.67))
    cv2.waitKey(125)

    while True:
        cv2.imshow('Squid game',cv2.resize(winner,(0,0),fx=0.67,fy=0.67))
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break

cv2.destroyAllWindows()






