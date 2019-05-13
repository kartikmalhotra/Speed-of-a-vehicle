import cv2
import numpy as np
import time
x1=10
y1=400
x2=1500
y2=400
x3=10
y3=550
x4=1500
y4=550
r=0
fps=202.16939577711565#frames per second calculayed in previous program
list1=[]
list2=[]
c1=0
start=0
end=0
cap = cv2.VideoCapture("videos/ax.mp4")
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#print (total)
subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows = False)
 
while True:
    _, frame = cap.read()
    start=time.time()
    cv2.line(frame, (x1,y1), (x2, y2), (0, 0xFF, 0), 3)
    cv2.line(frame, (x3,y3), (x4, y4), (0, 0xFF, 0), 3)
    mask = subtractor.apply(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.bitwise_and(gray, gray, mask= mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # Fill any small holes
    closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
    # Remove noise
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    # Dilate to merge adjacent blobs
    res = cv2.dilate(opening, kernel, iterations = 2)

   
    
    _, cnts, _ = cv2.findContours(res.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:9] # get largest five contour area
    rects = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        if h>= 10 and h<=15:
            rect = (x, y, w, h)
            centerx=int(x+w/2)
            centery=int(y+h/2)
            list2.append([centerx, centery])
            
            cv2.circle(frame,(centerx, centery), 3, (0,0,255), -1)
            if(centery<410 and centery>390 and centerx<600):
                cv2.line(frame, (x1,y1), (x2, y2), (0, 0, 0xFF), 3)
                list1.append([centerx, centery])
                c1=1
                start=time.time()
            if(centery>640 and centerx<560 and centerx<600):
                cv2.line(frame, (x3,y3), (x4, y4), (0, 0, 0xFF), 3)
                #print(r)
                end=time.time()
                #print(end-start)
                f=end-start
                no=float(r/fps)
                #print(no)
                print(int((5*18)/(no*5)))
                c1=0
                
                #print(end-start)
            rects.append(rect)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1);
        itr1=iter(list1)
        itr2=iter(list2)
  
               
    
    cv2.imshow("Frame", frame)
    cv2.imshow("res", res)
   
    
    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
