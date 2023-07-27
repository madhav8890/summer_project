from cvzone.HandTrackingModule import HandDetector
handModel = HandDetector(maxHands=1)
import cv2
import os
cap = cv2.VideoCapture(0)
while True:
    status , photo = cap.read()
    hand  = handModel.findHands(photo, draw=False )

    if hand:
        totalFinger = handModel.fingersUp(hand[0])
    
        if totalFinger == [ 1 , 0 , 0 , 0 , 0]:
            print("thumps up")
        
        elif totalFinger == [ 0 , 1 , 0 , 0 , 0]:
            print("index finger")
            os.system("chrome")
        
        
        elif totalFinger == [ 0 , 0 , 1 , 0 , 0]:
            print("middle finger")
            os.system("notepad")
    
    
        else:
            print("nothing")
            break
            
cap.release()