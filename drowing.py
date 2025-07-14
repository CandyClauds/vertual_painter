from time import sleep
import time
import cv2
import mediapipe
import cvzone
from math import *
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from numpy.ma.core import array
cam = cv2.VideoCapture(0)

cam.set(3, 1280)
cam.set(4, 720)
cam.set(10, 150)

dotlist = []
picture = []
#itten = cv2.imread("itten.png")
c = []
#resized = cv2.resize(itten, (700, 700), interpolation=cv2.INTER_AREA)

detector = HandDetector(detectionCon=0.8, maxHands=1)
dotlist = []


color = (0, 0, 0)


def drowingnow(dotlist):
    if len(dotlist)>=2:
        for dot in range(1, len(dotlist)):
            cv2.circle(imgResult, (dotlist[dot][0], dotlist[dot][1]), 10, dotlist[dot][2], cv2.FILLED)
            cv2.line(imgResult,(dotlist[dot-1][0], dotlist[dot-1][1]),(dotlist[dot][0], dotlist[dot][1]), dotlist[dot][2], 20)

def drowingall(picture):
    for lists in picture:
        drowingnow(lists)

def fing(hand):
    dis = []
    if int(dist(hand[0]['lmList'][4], hand[0]['lmList'][5])) < 70:
        dis.append(0)
    else:
        dis.append(1)

    for i in range(1, 5):
        if int(dist(hand[0]['lmList'][1+4*i], hand[0]['lmList'][4+4*i])) <80:
            dis.append(0)
        else:
            dis.append(1)
    return dis




while True:
    sun, img = cam.read()
    img = cv2.flip(img, 1)
    hands = detector.findHands(img, False)
    imgResult = img.copy()
    hand = hands[0]
    if hand:
        x, y, _ = hand[0]['lmList'][8]
        x1, y1, _ = hand[0]['lmList'][7]
        fingers = fing(hand)

        if 30 <x <1250 and 50 < y <960:

            if fingers == [0, 1, 0, 0, 0]:
                dotlist.append([x, y, color])

            elif fingers[1] != [0, 1, 0, 0, 0]:
                cv2.circle(imgResult, (x, y), 15, color, 3)
                picture.append(dotlist)
                dotlist = []




            if fingers == [1, 1, 1, 1, 1]:
                #copy = imgResult.copy()
                #copy[360-350:360+350, 640-350:640+350] = resized
                #imgResult = cv2.addWeighted(copy, 0.4, imgResult, 1 - 0.4, 0)
                if x-x1!=0:
                    if x-x1>=0:
                        distans = 35
                    else:
                        distans = -35

                    claimx=int(x+ cos(atan((y-y1)/(x-x1)))*distans )
                    claimy=int(y+ sin(atan((y-y1)/(x-x1)))*distans )

                    cv2.circle(imgResult, (claimx, claimy), 5, color, 3)
                    col = []
                    for n in str(imgResult[claimy, claimx])[1:-1].split(" "):
                        if n != "":
                            col.append(int(n))
                    color = tuple(col)

            drowingall(picture)
            drowingnow(dotlist)

            if fingers == [0,0,0,0,0]:
                sleep(2)
                isWritten = cv2.imwrite(f"{int(time.time())}.png", imgResult)
                sleep(2)


    cv2.imshow("cam", imgResult)
    cv2.waitKey(1)