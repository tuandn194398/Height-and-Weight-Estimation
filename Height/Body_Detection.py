# from _typeshed import SupportsWrite
import cv2 as cv
import mediapipe as mp
from playsound import playsound
import numpy as np
import pyttsx3
import pygame
import time
import math
from numpy.lib import utils

mpPose = mp.solutions.pose
mpFaceMesh = mp.solutions.face_mesh
facemesh = mpFaceMesh.FaceMesh(max_num_faces=2)
mpDraw = mp.solutions.drawing_utils
drawing = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
pose = mpPose.Pose()
capture = cv.VideoCapture(f"http://10.9.4.6:4747/video")
lst = []
n = 0
scale = 3
ptime = 0
count = 0
brake = 0
x = 150
y = 195
h_screen = 350 / 50100 # chiều cao thực toàn bộ tầm nhìn ảnh là 350 cm, chiều cao khung ảnh là 720 pixels
num = 0

while True:
    isTrue, img = capture.read()
    img_rep = img
    # img = cv.imread("img10.jpg")
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    new_width_img = int(720 / img.shape[0] * img.shape[1])
    # print("new width: ", new_width_img)
    img = cv.resize(img, (668, 501))
    result = pose.process(img_rgb)
    if result.pose_landmarks:
        mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # danh sách tọa độ điểm ở chân
        lst_3132 = []
        for id, lm in enumerate(result.pose_landmarks.landmark):
            print("id: " + str(id))
            lst[n] = lst.append([id, lm.x, lm.y])
            n + 1
            # print(lm.z)
            # if len(lst)!=0:
            #     print(lst[3])
            h, w, c = img.shape
            # id = 32 là chân trái, 31 là chân phải
            if id == 32 or id == 31:
                cx1, cy1 = int(lm.x * w), int(lm.y * h)
                # hình tròn màu đen ở chân
                cv.circle(img, (cx1, cy1), 15, (0, 0, 0), cv.FILLED)
                # print("Center: " + str(cx1) + "/" + str(cy1))
                print(str(id) + "Distance: " + str(h - cy1))
                if (h - cy1) > 0 and (w - cx1) > 0:
                    lst_3132.append([cx1, cy1])
                print("********************************")
                # tinh khoang cach
                # d = ((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2) ** 0.5
                # di = round(d * 0.3)
                dom = ((lm.z - 0) ** 2 + (lm.y - 0) ** 2) ** 0.5
                # height = round(utils.findDis((cx1,cy1//scale,cx2,cy2//scale)/10),1)

                cv.putText(img, "Height : ", (40, 70), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), thickness=2)
                # cv.putText(img, str(di), (180, 70), cv.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), thickness=2)
                cv.putText(img, "cms", (240, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), thickness=2)

            if id == 6:
                cx2, cy2 = int(lm.x * w), int(lm.y * h)
                # cx2 = cx230
                cy2 = cy2 + 20
                cv.circle(img, (cx2, cy2), 15, (0, 0, 0), cv.FILLED)

            print("lst: " + str(lst_3132))
            if len(lst_3132) == 1:
                d = ((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2) ** 0.5
                dept = h - cy1
                print("dept: " + str(dept))
                di = round(d * h_screen * dept)
                print("di: " + str(di))
                # di_last = di
                di_last = int(di * 1.1+3)
                print("di_last: " + str(di_last))
                # while di_last < 155 or di_last > 200:
                #     di_last = di_last + di
                #     if di_last > 200:
                #         di = di / 2
                #         di_last = di_last * 0.05
                cv.putText(img, "Stand at least 3 meter away: " + str(dept) + "/100", (40, 450), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 255), thickness=2)
                cv.putText(img, str(di_last), (180, 70), cv.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), thickness=2)
            if len(lst_3132) == 2:
                xl, yl = lst_3132[0]
                xr, yr = lst_3132[1]
                if max(yl, yr) == yl:
                    d = ((cx2 - xl) ** 2 + (cy2 - yl) ** 2) ** 0.5
                    dept = h - yl
                else:
                    d = ((cx2 - xr) ** 2 + (cy2 - yr) ** 2) ** 0.5
                    dept = h - yr
                di = round(d * h_screen * dept)
                # di_last = di
                di_last = int(di * 1.1+3)
                print("di_last: " + str(di_last))
                # while di_last < 155 or di_last > 200:
                #     di_last = di_last + di
                #     if di_last > 200:
                #         di = di / 2
                #         di_last = di_last * 0.05
                print("dept: " + str(dept))
                print("di: " + str(di))
                cv.putText(img, str(di_last), (180, 70), cv.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), thickness=2)
                cv.putText(img, "Stand at least 3 meter away: " + str(dept) + "/100", (40, 450), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 255), thickness=2)

    # img = cv.resize(img, (700, 500))
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv.putText(img, "FPS : ", (40, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), thickness=2)
    cv.putText(img, str(int(fps)), (160, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), thickness=2)
    cv.imshow("Task", img)
    print("Last shape: ", img.shape)
    if cv.waitKey(1) & 0xFF == ord('s'):
        cv.imwrite('./image_input/imageRaw' + str(num) + '.png', img_rep)
        cv.imwrite('./image_input/imageHeight' + str(num) + '.png', img)
        num += 1
        print('Images saved')
    elif 0xFF == ord('q'):
        break
capture.release()
cv.destroyAllWindows()
