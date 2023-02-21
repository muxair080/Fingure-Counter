import cv2
import time
import os
import handTrackingModule as htm

# Trun on camera
cap = cv2.VideoCapture(0)

# set width and height of camera window
wCam, hCam = 640, 480

cap.set(3, wCam)
cap.set(3, hCam)

folderPath = 'images'
myList = os.listdir(folderPath)
overlayList = []
print(myList)

# reading images from folder
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    image = cv2.resize(image,(200,200))
    overlayList.append(image)

print(overlayList)
print('len : ',len(overlayList))
cTime = 0
pTime=0

# creating module oject
detector = htm.handDetector(detectionCon=0.75)
# top point id's of all fingures
# 4 for tumb top
# 8 index/first fingure top
# 12 middle fingure top
# 16 ring fingure top
# 20 for little/pinky fingure top

tipIds = [4,8,12,16,20]

while True:
    # read image
    success, img = cap.read()
    # this function detect hand
    img = detector.findHands(img)
    # find landmarks positions in fingures
    lmList = detector.findPosition(img, draw=False)
    # print(lmList) 

    # if landmarks exists then this code will be run

    if len(lmList) !=0:
        """ this condition means if height is increasing then
        its value will be in landmark smaller and vise versa 
        e.g is one landmark in 50 and other is 100 so 50 landmark 
        point is occuring above the 100 landmark point."""
        fingers = []
        # tumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1 ][1]:
                # print('Index fingure open')
            fingers.append(1)
        else:
            fingers.append(0)
            # for remaining four fingures
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                # print('Index fingure open')
                fingers.append(1)
            else:
                fingers.append(0)
                # print('Index fingure close')
        
        totalFingures = fingers.count(1)
        print(totalFingures)



        h,w,c = overlayList[0].shape
        img[0:h, 0:w] = overlayList[totalFingures]
        cv2.rectangle(img, (20,255),(170,400), (0,255,0),
         cv2.FILLED)
        cv2.putText(img, str(totalFingures), (45,375),
         cv2.FONT_HERSHEY_PLAIN,
        10, (255,0,0), 25)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS : {int(fps)}',(400,70), cv2.FONT_HERSHEY_COMPLEX,
    1, (255,0,0),3)

    cv2.imshow('Image', img)
    # cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
cap.release()
cv2.destroyAllWindows()
