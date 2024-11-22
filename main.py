import HandTmodule as htm
import time
import cv2
import math
import numpy as np
import pandas as pd
import regress as rg

noNew = True
def dataCollect(capdevice=0, point=[0], drawHand=True, drawPoint=True,):
        cap = cv2.VideoCapture(capdevice)
        detector = htm.hDetector()
        rest = []
        lastime = time.time()
        speak = "Start COnfig?"
        midDone = False
        readingHigh = False
        prompt = False
        lowData = []
        highData = []
        midData = []
        readingMid = False
        mid = False
        while True:
                succ, img = cap.read()
                img = detector.find(img, drawHand)
                lmLis = detector.findPos(img, drawPoint, point)
                

                if len(lmLis) != 0:
                        lis = [lmLis[dot][1:] for dot in point]
                        distance = math.sqrt((lis[1][0] - lis[0][0])**2 + (lis[1][1] - lis[0][1])**2)
                        if len(rest) < 2:
                                rest.append(distance)
                        else:
                                arr = np.array(rest)
                                # print(rg.call(int(round(np.mean(arr),2)*100)))
                                if prompt:
                                        if time.time() - lastime > 3:
                                                speak = "Analyzing.."
                                        lowData.append(int(round(np.mean(arr),2)*100))
                                        if time.time()-lastime > 9:
                                                print(lowData)
                                                prompt = False
                                                mid = True
                                if readingMid:
                                        if time.time() - lastime > 3:
                                                speak = "Analyzing.."
                                        midData.append(int(round(np.mean(arr),2)*100))
                                        if time.time()-lastime > 9:
                                                print(midData)
                                                readingMid = False
                                                midDone = True
                                if readingHigh:
                                        if time.time() - lastime > 3:
                                                speak = "Analyzing.."
                                        highData.append(int(round(np.mean(arr),2)*100))
                                        if time.time()-lastime > 9:
                                                print(highData)
                                                cv2.destroyAllWindows()
                                                noNew = False
                                                break
                                rest = []

                

                cv2.putText(img, speak, (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 5), 3)
                key = cv2.waitKey(1)
                if key == ord('y'):
                        noNew = True
                        speak = "close index finger and thumb"
                        prompt = True
                        lastime = time.time()
                if key == ord('n'):
                        cv2.destroyAllWindows()
                        break
                if mid:
                        speak = "half open index finger and thumb"
                        lastime = time.time()
                        mid = False
                        readingMid = True
                if midDone:
                        speak = "max open index finger and thumb"
                        lastime = time.time()
                        midDone = False
                        readingHigh = True

                cv2.imshow("image",img)
                cv2.waitKey(1)
        return[lowData, midData,highData]



cam = 0

data = dataCollect(point=[4,8], capdevice=cam)


if not noNew:
        df1 = pd.DataFrame([(x,0) for x in data[0]])
        df2 = pd.DataFrame([(x,0.5) for x in data[1]])
        df3 = pd.DataFrame([(x,1) for x in data[2]])
        pd.concat([df1,df2,df3]).to_csv('allData.csv', index=False, header = False)
        rg.newWeights()
htm.run(point=[4,8], capdevice= cam)
