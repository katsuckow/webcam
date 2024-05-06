import cv2 as cv
import numpy as np

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

#mmpi2 = document
def align (x, rotated):
    document = x
    frame_s = rotated

#########################
# Transform document to gray
#########################
    try:
        document_gray = cv.cvtColor(document, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(document_gray, 170,250,cv.THRESH_BINARY) 

#######################
#Find all Contours
#######################
        contours3, hierarchy3 = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        document_copy = document.copy()
        document_copy1 = document.copy()

#####################
#draw alle Contours
#####################

        for contour in contours3:
            cv.drawContours(document_copy, contour, -1, (0,255,0),1)

#####################
#Write all contours in variable "all_areas"
#####################

        all_areas = []

        for cnt in contours3:
            area = cv.contourArea(cnt)
            all_areas.append(area)

####################
#sort contours by size
#identify biggest contour and draw
####################
        sorted_contours = sorted(contours3, key = cv.contoursArea, reverse = True)
        largest_item = sorted_contours[0]

###################
# draw a straight line around the edges of the biggest contour and export result
###################

        perimeter = cv.arcLength(largest_item, True)
        approx = cv.approxPolyDP(largest_item, 0.1 * perimeter, True)

        for point in approx:
            x,y = point[0]
            cv.circle(document_copy1, (x,y), 3, (0,255,0), -1)

##################
#draw skewed rectangle
##################
        cv.drawContours(document_copy1, [approx], -1, (0,255,0), 5)

#################
#correct for skewed document
#################

        #print(approx)
        print(np.float32(approx[0,0,1]), np.float32(approx[1,0,1]), "coordinates")
        
        if(np.float32(approx[0,0,0]) > np.float32(approx[0,0,1])):
            pt_A = np.float32(approx[1,0,0:])
            pt_B = np.float32(approx[0,0,0:])
            pt_C = np.float32(approx[3,0,0:])
            pt_D = np.float32(approx[2,0,0:])
            input_pts = np.float32([pt_A,pt_B,pt_C,pt_D])
            output_pts = np.float32([[0,0],
                                     [0,frame_s[0]],
                                     [frame_s[1],frame_s[0]],
                                     [frame_s[1],0]])
        else:
            print(frame_s,"Frame", frame_s[1], frame_s[0], type(frame_s))
            pt_A = np.float32(approx[0,0,0:])
            pt_B = np.float32(approx[1,0,0:])
            pt_C = np.float32(approx[2,0,0:])
            pt_D = np.float32(approx[3,0,0:])
            input_pts = np.float32([pt_A,pt_B,pt_C,pt_D])
            output_pts = np.float32([[0,0],
                            [0,frame_s[1]],
                            [frame_s[0],frame_s[1]],
                            [frame_s[0],0]])
        
        input_pts = np.float32([pt_A,pt_B,pt_C,pt_D])
        output_pts = np.float32([[0,0],
                            [0,frame_s[0]],
                            [frame_s[1],frame_s[0]],
                            [frame_s[1],0]])
        
        M = cv.getPerspectiveTransform(input_pts, output_pts)

###########################
#perpective transform using homography
###########################
        final = cv.warpPerspective(document_copy1, M, (frame_s[0]), flag = cv.INTER_LINEAR)
        scale2 = final.copy()

    except:
        document_gray = cv.cvtColor(document)
        thresh2 = cv.adaptiveThreshold(document_gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 21, 10)
        scale_2 = thresh2.copy()

    return document_copy1, scale_2

cam = cv.VideoCapture(0)

while True:
    check, frame = cam.read()
    frame_original = np.array(frame)
    frame_rotated = cv.rotate(frame_original, cv.ROTATE_90_CLOCKWISE)
    center_x = int(frame.shape[1]/2)
    x_width = int(frame.shape[0]/1.41)
    x_half = x_width/2
    x1 = center_x - x_half
    x2 = center_x + x_half

######################
#include pytesseract to extract writing from document in scence
#adaptive threshold to clean noisy image
#pytesseract and return detected text from in window
######################

    frame1 = frame[0:int(frame.shape[0]), int(x1):int(x2)]
    
    frame2, aligned = align(frame,frame1.shape)

    cv.imshow('video', frame)

    key = cv.waitKey(1)
    if key == 27:
        cv.imshow("Aligned", aligned)
        cv.waitKey(0)
        cv.destroyAllWindows
        break

cam.release()
cv.destroyAllWindows