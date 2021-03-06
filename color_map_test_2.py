import cv2
from math import sqrt
import copy
from moving_average import MovingAvg
from serial_device import SerialDevice
from time import sleep, time

arduino = SerialDevice()
# define a video capture object
vid = cv2.VideoCapture(0)


mean_area = MovingAvg(10, 20)
mean_center_x = MovingAvg(10, .5)
mean_center_y = MovingAvg(10, .5)
prev_time = time()
while(True):
    # Capture the video frame
    # by frame
    ret, img = vid.read()

    scale_percent = .5
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    img = cv2.flip(cv2.resize(img, (width, height)), -1)
    img_copy = copy.deepcopy(img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange (hsv, (4, 72, 100), (13, 255, 180))
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    target_area = (width // 2) * (height // 2)
    
    if contours:
        #if any contours are found we take the biggest contour and get bounding box
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
        #compute area and center point
        box_area = box_width*box_height

        show = box_area > target_area // 6
        # print(box_area)
        if show:
            (center_x,center_y) = ((2*x_min + box_width)/2, (2*y_min + box_height)/2)
            # print((center_x,center_y))

            # while not mean_area.full():
            mean_area.push(box_area)
            # while not mean_center_x.full():
            mean_center_x.push(center_x)
            # while not mean_center_y.full():
            mean_center_y.push(center_y)

            x_offset = mean_center_x.avg - (width // 2)
            center_offset_x = abs(x_offset)
            turn_direction = 1 if x_offset > 0 else -1
            angle = center_offset_x/(width // 2)
            # print(angle, direction)

            
            area_offset = mean_area.avg - target_area
            
            if area_offset < 0:
                if turn_direction <= 0:
                    direction = "forward" if angle <= .25 else "left"
                else:
                    direction = "forward" if angle <= .25 else "right"
            else:
                direction = "stay"
            
            if time() - prev_time > 2:
                prev_time = time()
                print(direction)
                print("Angle {}: ".format(angle))
                print(turn_direction)
                arduino.write(direction)
        

        # if arduino.ser.in_waiting:
        #     line = arduino.read()
        #     if line.strip() != '':
        #         print("Arduino thing: {}".format(line))


        #if mean_area.full() and mean_center_x.full() and mean_center_y.full():
         #   side_length_half = sqrt(mean_area.avg) / 2
          #  top_left  = (int(mean_center_x.avg - side_length_half), int(mean_center_y.avg - side_length_half))
           # bottom_right = (int(mean_center_x.avg + side_length_half), int(mean_center_y.avg + side_length_half + 15))
            #drawing a rectangle around the object with 15 as margin
   #         if show:
    #            cv2.rectangle(img, (x_min - 15, y_min - 15),
     #                       (x_min + box_width + 15, y_min + box_height + 15),
      #                      (0,255,0), 4)
       #     cv2.rectangle(img_copy, top_left,
        #        bottom_right,
         #       (0,255,0), 4)

    # Display the resulting frame
#    cv2.imshow('unfiltered', img)
 #   cv2.imshow('filtered', img_copy)
    #cv2.imshow('hsv', hsv)
  #  cv2.imshow('mask', mask)

      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
