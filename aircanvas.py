import cv2
import numpy as np
import time
import os
import handtracking as htm

#######################
brushthickness=22
eraserthickness=50

#######################

# #for choosing the photos
# def make_720p():
#     cap.set(3, 500)
#     cap.set(4, 135)

folderpath="header"
myList=os.listdir(folderpath)
print(myList)
overlayList=[]
for impath in myList:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlayList.append(image)
print(len(overlayList))
header=overlayList[0]
drawColor=(255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,1260)
cap.set(4,720)

#assigning handtracking module
detector = htm.handDetector(detectionCon=0.85)
xp,yp=0,0
imgcanvas=np.zeros((720,1280,3),np.uint8)

while True:
    #1)import image
    success, img = cap.read()
    img = cv2.flip(img,1)

    #2. find the landmarks

    img= detector.findHands(img) #showing handdetector over the image
    lmList = detector.trackPos(img, draw=False)

    if len(lmList) != 0:
        xp,yp=0,0

        #print(lmList)

        #tip points for index and middle finger

        x1, y1= lmList[8][1:]
        x2, y2= lmList[12][1:]





    # 3)check which fingers are up

        fingers = detector.fingersUp()
        # print(fingers)


    # 4)if selectioon mode-2 fingers up
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            #FOR MAKING CIRCLE
            cv2.rectangle(img, (x1,y1-25), (x2,y2+25), drawColor,cv2.FILLED )
            print("selection mode")
            if y1<125:
              if 0<x1<100:
                header= overlayList[0]
                drawColor = (255, 0, 255)
              if 100<x1<200:
                header= overlayList[1]
                drawColor = (255, 0, 0)
              if 200<x1<300:
                header= overlayList[2]
                drawColor = (0, 255, 0)
              if 300<x1<400:
                header= overlayList[3]
                drawColor = (0, 0, 0)
        cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)


    # 5)if drawing mode 1 finger up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            print("drawing mode")

            if xp==0 and yp==0:
                xp,yp=x1,y1

                if drawColor==(0,0,0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushthickness)
                    cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, brushthickness)


            #starting and ending position of line
                else:
                   cv2.line(img ,(xp ,yp),(x1,y1) ,drawColor,brushthickness)
            #to draw on canvas instead of img
                   cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, brushthickness)

            xp,yp= x1,y1

    # imgGray = cv2.cvtColor(imgcanvas, cv2.COLOR_BGR2GRAY)
    # _, imgInverse = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    # imgInverse = cv2.cvtColor(imgInverse, cv2.COLOR_GRAY2BGR)
    #
    # img = cv2.bitwise_and(img, imgInverse)
    # img = cv2.bitwise_or(img, imgcanvas)






# 6)setting the header image
    img[0:62,0:500]=header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("image",img)
    cv2.imshow("canvas", imgcanvas)
    # cv2.imshow("canvas", imgInverse)
    cv2.waitKey(1)



