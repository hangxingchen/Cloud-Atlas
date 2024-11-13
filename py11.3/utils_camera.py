# utils_camera.py
# HANG
# Open the camera, display real-time video feed, press 'q' to exit

import cv2
import numpy as np

def check_camera():
    '''
    Open the camera, display real-time video feed, press 'q' to exit
    '''
    print('Opening the camera...')
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        # Uncomment the line below if you want to display the frame in grayscale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
