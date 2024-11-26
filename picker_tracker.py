import cv2
import numpy as np

# cap = cv2.VideoCapture(r"C:\Users\mhmdf\Desktop\gait_1.mp4")

cap = cv2.VideoCapture(r"C:\Users\mhmdf\Downloads\174_48-SL.mp4")
# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)
# cap.set(10,150)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_174_48-SL.avi', fourcc, 20.0, (1920, 1080))

def empty(a):
    pass


cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",640,280)
cv2.createTrackbar("Hue Min","Trackbars",0,179,empty)
cv2.createTrackbar("Hue Max","Trackbars",0,179,empty)
cv2.createTrackbar("Sat Min","Trackbars",0,255,empty)
cv2.createTrackbar("Sat Max","Trackbars",0,255,empty)
cv2.createTrackbar("Val Min","Trackbars",0,255,empty)
cv2.createTrackbar("Val Max","Trackbars",0,255,empty)
cv2.createTrackbar("draw", "Trackbars", 0, 1, empty)

def drawOnCanvas(myPoints): 
    # for point in myPoints: 
    #     cv2.circle(img, (point[0], point[1]), 
    #                5, (0,0,255), cv2.FILLED)
    r=1
    g=255
    b=255
    if len(myPoints)>1:
        for i in myPoints:
            if myPoints.index(i)>=1:
                cv2.line(img, myPoints[myPoints.index(i)-1], i,(r,g,b),4)
                # r+=1
                # g-=1
                # b+=1

pointlist=[]

while True:
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max","Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min","Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max","Trackbars")
    v_min = cv2.getTrackbarPos("Val Min","Trackbars")
    v_max = cv2.getTrackbarPos("Val Max","Trackbars")
    draw = cv2.getTrackbarPos("draw","Trackbars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    # 178,168


    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    yellow_mask = cv2.inRange(imgHSV,lower,upper)
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
            cv2.line(img,(mid1,0),(mid1,1080),(255,0,255),2)
            cv2.line(img,(0,mid2),(1920,mid2),(255,0,255),2)
            cv2.circle(img, (mid1, mid2), 
                   5, (255,0,0), cv2.FILLED)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # pointlist.append([mid1,mid2])
            if draw:
                pointlist.append([mid1,mid2])
                drawOnCanvas(pointlist)
                
            
            break

    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("Video",img)
    cv2.imshow("Mask",mask)
    if draw:
        out.write(img)
    #cv2.imshow("Result",imgResult)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break