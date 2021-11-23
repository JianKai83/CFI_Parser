import cv2
import numpy as np
import PoseModule as pm
import pandas as pd

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
count_t=0
dir =1
nu = 0
tmp = 0
angle_elbow_DF = []
angle_body_DF = []


while (cap.isOpened()):
    success, img = cap.read()
    if (success != True):
        break

    if tmp == 0:
        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # wrt = cv2.VideoWriter('good'+ str(nu) +'.mp4', fourcc, 10.0, (1280, 720))
        tmp+=1
        nu +=1
        angle_elbow_list = []
        angle_body_list = []

    img = cv2.resize(img,(1280,720))
    img = detector.findPose(img,False)

    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        #Right Arm
        angle_elbow = detector.findAngle(img, 12,14,16)
        angle_elbow_list.append(angle_elbow)

        #Body
        angle_body = detector.findAngle(img, 12, 24, 26)
        angle_body_list.append(angle_body)

        per = np.interp(angle_elbow,(70, 150),(0,100))

        #dir =1 代表行程往上
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        if per ==100:
            if dir ==0:
                count += 0.5
                dir = 1

    cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                (255, 0, 0), 25)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # wrt.write(img)

    if (count-count_t)==1:
        # wrt.release()
        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # wrt = cv2.VideoWriter('good'+ str(nu) +'.mp4', fourcc, 10.0, (1280, 720))
        nu+=1
        count_t+=1
        angle_elbow_DF.append(angle_elbow_list)
        angle_body_DF.append(angle_body_list)
        angle_elbow_list=[]
        angle_body_list = []

    if cv2.waitKey(5) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

df_elbow = pd.DataFrame(angle_elbow_DF)
df_body = pd.DataFrame(angle_body_DF)
df_elbow.to_csv('Biceps_Curl_elbow_good.csv',index=False)
df_body.to_csv('Biceps_Curl_body_good.csv',index=False)