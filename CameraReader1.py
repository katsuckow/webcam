import cv2 as cv
import numpy as np

import pytesseract
from pytesseract import Output

# you have to have tesseract installed
# Usual address for tesseract in Windows is like
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

#switch on camera
video = cv.VideoCapture(0)

# count frames that have been generated
a = 1

# repeatedly build pictures for 3s
while True:
    a = a + 1 
    # build a frame to display webcam picture
    # check: boolean datatype, frame: numpy array
    check, frame = video.read()
    print(check)
    print(frame)
#    print(a)

    # converting frame picture into gray image
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # blur results 
    blur = cv.medianBlur(gray,1)
    blur = blur

    # adaptive threshold in noisy environment
    # adThr = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 45)
    adThr = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 12)
    custom_config = r'--oem 3 --psm 6'
    x = pytesseract.image_to_string(adThr, config=custom_config, lang="eng")
    y = pytesseract.image_to_data(adThr, output_type=Output.DICT)
    print(y)
    print(x)
    print(len(x))

    cv.putText(adThr, x, (100,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv.LINE_AA)
    cv.imshow("Capturing",adThr)


    key = cv.waitKey(1)

    if key == ord('q'):
        
        break
    

video.release()

cv.destroyAllWindows()

