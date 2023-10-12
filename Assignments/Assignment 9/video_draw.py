#! /usr/bin/env python
import numpy as np 
import cv2

#0-primary camera
#1-external camera
#path
video=cv2.VideoCapture('avengers.mp4')

#reading frame
while(True):
    ret,frame=video.read()
    cv2.line(frame,(0,0),(300,300),(255,255,255),3)
    cv2.rectangle(frame,(100,100),(400,500),(0,255,0),3)    
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindow()