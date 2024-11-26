import cv2
from PIL import Image as pilImage
import numpy as np


lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])
# self color list
colors = [(255,0,0),(0,255,0),(0,0,255)]

def main():
    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(r"C:\Users\mhmdf\Desktop\gait_1.mp4")
    cap = cv2.VideoCapture(r"C:\Users\mhmdf\Downloads\188__1_8.mp4")
    

    while True:
        succes, img = cap.read() 
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv_image,  lower_green,  upper_green)
        bbox_green = pilImage.fromarray(green_mask).getbbox()

        if bbox_green is not None:
            x1,y1,x2,y2 = bbox_green
            center_green_x = (x1 + x2) // 2
            center_green_y = (y1 + y2) // 2
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 5)
            cv2.circle(img, (center_green_x, center_green_y), 5, (0,255,0), 3)
        
        cv2.imshow('img', img)
             
        if cv2.waitKey(100) & 0xff == ord('q'): 
            break



if __name__=="__main__":
    main()


# import cv2
# # cap = cv2.VideoCapture(0)


# cap = cv2.VideoCapture(r"C:\Users\mhmdf\Downloads\188__1_8.mp4")
# # cap = cv2.VideoCapture(r"C:\Users\mhmdf\Desktop\gait_1.mp4")
# # tracker = cv2.TrackerMOSSE_create()
# # tracker = cv2.legacy.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()

# success,img = cap.read()
# bbox = cv2.selectROI('Tracker',img,False)
# tracker.init(img,bbox)

# def drawBox(img,bbox):
#     x, y, w, h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
#     cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
#     cv2.putText(img,"tracking",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)


# while True:
#     success,img = cap.read()
#     timer = cv2.getTickCount()
#     success,bbox = tracker.update(img)

#     if success :
#         drawBox(img,bbox)
#     else:
#         cv2.putText(img,"lost",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,0),2)

        

#     fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
#     cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
#     cv2.imshow('output',img)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break
