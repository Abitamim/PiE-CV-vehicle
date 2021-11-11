import cv2
import numpy as np
import math
from queue import Queue
class MovingAvg:

    def __init__(self, max_vals = 10, threshold = .1):
        self.values = Queue(max_vals)
        self.avg = 0
        self.sum = 0
        self.threshold = threshold
        
    def push(self, val):
        if self.values.full():
            self.sum -= self.values.get()
        
        self.values.put(val)
        self.sum += val
        self.avg = self.sum / self.values.qsize()

        return self.avg

    def avg(self):
        return self.avg
    
    def full(self):
        return self.values.full()

    def withinBounds(self, val):
        return self.avg * (1 + self.threshold) >= val and self.avg * (1 - self.threshold) <= val

# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, img = vid.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange (hsv, (0, 170, 100), (50, 255, 255))
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    
    if contours:
        #if any contours are found we take the biggest contour and get bounding box
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
        #compute area and center point
        box_area = box_width*box_height
        # print(box_area)
        (center_x,center_y) = ((2*x_min + box_width)/2, (2*y_min + box_height)/2)
        # print((center_x,center_y))
        
        mean_area = MovingAvg(10, .01)
        mean_center_x = MovingAvg(10, .01)
        mean_center_y = MovingAvg(10, .01)
        while not mean_area.full():
            mean_area.push(box_area)
        while not mean_center_x.full():
            mean_center_x.push(center_x)
        while not mean_center_y.full():
            mean_center_y.push(center_y)
        if mean_area.full() and mean_center_x.full() and mean_center_y.full():
            print(mean_area.values.queue)
            if mean_area.withinBounds(box_area):
                if mean_center_x.withinBounds(center_x):
                    if mean_center_y.withinBounds(center_y):
                        mean_area.push(box_area)
                        mean_center_x.push(center_x)
                        mean_center_y.push(center_y)
                        #drawing a rectangle around the object with 15 as margin
                        cv2.rectangle(img, (x_min - 15, y_min - 15),
                                    (x_min + box_width + 15, y_min + box_height + 15),
                                    (0,255,0), 4)

    # Display the resulting frame
    cv2.imshow('frame', img)
    #cv2.imshow('hsv', hsv)
    cv2.imshow('mask', mask)

      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()