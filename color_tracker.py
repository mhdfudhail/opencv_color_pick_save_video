import cv2
import numpy as np

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(r"C:\Users\mhmdf\Downloads\188__1_8.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_188__1_8.avi', fourcc, 20.0, (1920, 1080))

# cap.set(2,340)
# cap.set(2,480)
# cap.set(10,150)
# height, width = c.shape[:2]
def drawOnCanvas(myPoints): 
    # for point in myPoints: 
    #     cv2.circle(img, (point[0], point[1]), 
    #                5, (0,0,255), cv2.FILLED)
    if len(myPoints)>1:
        for i in myPoints:
            if myPoints.index(i)>=1:
                cv2.line(img, myPoints[myPoints.index(i)-1], i,(255,0,255),4)

pointlist=[]

while True:
    success, img = cap.read()
    Gaussian = cv2.GaussianBlur(img, (7, 7), 0) 
   
    # Median Blur 
    median = cv2.medianBlur(img, 5) 
    
    # Bilateral Blur 
    bilateral = cv2.bilateralFilter(img, 9, 75, 75) 
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # red color
    # 32 178 118 255 182 255
    low_yellow = np.array([31, 78, 111])
    high_yellow = np.array([255, 166, 255])
    yellow_mask = cv2.inRange(imghsv,low_yellow,high_yellow)
    contours,hiuud = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(yellow_mask,cnt,-1,(255,0,255),2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            (x, y, w, h) = cv2.boundingRect(approx)
            
            mid1 = int((x+w/2))
            mid2 = int((y+w/2))
            # cv2.line(img,(mid1,0),(mid1,480),(255,0,255),2)
            # cv2.line(img,(0,mid2),(640,mid2),(255,0,255),2)
            # cv2.circle(img, (mid1, mid2), 
            #        5, (255,0,0), cv2.FILLED)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            pointlist.append([mid1,mid2])
            
            break



    drawOnCanvas(pointlist)
    cv2.imshow("output",img)
    cv2.imshow("mask",yellow_mask)
    # out.write(img)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
f = open("foot_points_2.txt", "w")
indexNum=0
for i in pointlist:
    f.write(F"{indexNum} : X:{i[0]}, Y:{i[1]}\n")
    indexNum+=1
f.close()
print("hello")