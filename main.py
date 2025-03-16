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
                        noNew = False
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

def remOut(data, threshold=1.5):
    if len(data) == 0:
        return np.array([])
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr
    return data[(data >= lower_bound) & (data <= upper_bound)]


cam = 0

data = dataCollect(point=[4,8], capdevice=cam)
values = [0, 0.5, 1]

if not noNew:
        cleaned = []
        for arr in data:
                cleaned.append(remOut(np.array(arr, dtype=float)))
        df1 = pd.DataFrame([(x, values[i]) for i in range(len(cleaned)) for x in cleaned[i]], columns=['dist', 'val'])
        df1.to_csv('allData.csv')
        rg.newWeights()
htm.run(point=[4,8], capdevice= cam)
