import cv2
import mediapipe as mp
import time
import math
import numpy as np
import regress as rg
import pyvolume


class hDetector():
    def __init__(self, mode=False, maxHands=1, detectConf=0.5, tracConf=0.5, modelComp = 1):
        self.mode = mode
        self.maxHand = maxHands
        self.detectConf = detectConf
        self.tracConf = tracConf
        self.modelComp=  modelComp

        self.pHands = mp.solutions.hands
        self.hands = self.pHands.Hands(self.mode, self.maxHand, self.modelComp, self.detectConf, self.tracConf)
        self.mDraw = mp.solutions.drawing_utils

    def find(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(imgRGB)


        if self.res.multi_hand_landmarks:
            for handLms in self.res.multi_hand_landmarks:
                    if draw:
                        self.mDraw.draw_landmarks(img,handLms, self.pHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, draw=True, point=[0]):
        lmLisH1 = []
        lmLisH2 = []
        newLis = []
        if self.res.multi_hand_landmarks:
            selHand1 = self.res.multi_hand_landmarks[0]
            for id, lms in enumerate(selHand1.landmark):
                        h,w,c = img.shape
                        cx, cy = int(lms.x*w), int(lms.y*h)
                        lmLisH1.append([id, cx, cy])
                        newLis.append([id, lms.x,lms.y])
            # if len(self.res.multi_hand_landmarks) > 1:
            #     selHand2 = self.res.multi_hand_landmarks[1]
            #     for id, lms in enumerate(selHand2.landmark):
            #                 h,w,c = img.shape
            #                 cx, cy = int(lms.x*w), int(lms.y*h)
            #                 lmLisH2.append([id, cx, cy])
            if draw:
                if len(lmLisH1) != 0:
                    [cv2.circle(img, lmLisH1[dot][1:], 10, (255,0,255), cv2.FILLED) for dot in point]
                # if len(lmLisH2) != 0:
                #     [cv2.circle(img, lmLisH2[dot][1:], 10, (0,255,255), cv2.FILLED) for dot in point]
        return newLis




def run(capdevice=0, point=[0], drawHand=False, drawPoint=False,):
    cap = cv2.VideoCapture(capdevice)
    pTime = 0
    cTime = 0
    detector = hDetector()
    lasVal = 0
    rest = []
    while True:
        succ, img = cap.read()
        img = detector.find(img, drawHand)
        lmLis = detector.findPos(img, drawPoint, point)
        if len(lmLis) != 0:
            lis = [lmLis[dot][1:] for dot in point]
            distance = math.sqrt((lis[1][0] - lis[0][0])**2 + (lis[1][1] - lis[0][1])**2)
            if len(rest) < 10:
                rest.append(distance)
            else:
                arr = np.array(rest)
                curVal = rg.call(round(np.mean(arr),2)*100)
                if curVal:
                    curVal = int(curVal)
                    if(abs(curVal-lasVal)>10):
                        lasVal = curVal
                        print(curVal)
                        if curVal > 100:
                             pyvolume.custom(percent=100)
                        else:
                             pyvolume.custom(percent=curVal)
                        
                # if rg.call(round(np.mean(arr),2)*100):
                
                rest = []

        cv2.waitKey(50)


# def main():
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#     cTime = 0
#     detector = hDetector()
#     while True:
#         succ, img = cap.read()
#         img = detector.find(img)
#         lmLis = detector.findPos(img, draw=False)
#         if len(lmLis) != 0:
#              print(lmLis[4])
#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime
#
#         cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
#
#         cv2.imshow("image",img)
#         cv2.waitKey(1)



if __name__ == "__main__":
    run(point=[4,8])