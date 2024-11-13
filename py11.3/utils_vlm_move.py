# utils_vlm_move.py
# Input commands: Multimodal large model recognizes the image, robotic gripper picks up and moves the object

# print('Kobe University')

from utils_robot import *
from utils_asr import *
from utils_vlm import *

import time

def vlm_move(PROMPT='Please move the green block onto my hand', input_way='keyboard'):
    '''
    Multimodal large model recognizes the image, and the robotic arm picks up and moves the object.
    input_way: 'speech' for voice input, 'keyboard' for keyboard input
    '''

    print('Multimodal large model recognizes the image, robotic arm picks up and moves the object')
    
 
    

    print('Moving the robotic arm to the zero position')
    pwm_values = [1500, 1500, 1500, 1500, 1610, 1500]  # Specified PWM pulse widths

    for i, pwm in enumerate(pwm_values):
        pca.setServoPulse(i, pwm)  # Set the PWM pulse width for the corresponding channel
        print(f'Set PWM pulse width for channel {i} to {pwm}')

    time.sleep(3)  # Pause for 3 seconds to ensure the arm completes the movement




    ## Step 1: Perform hand-eye calibration
    print('Step 1: Performing hand-eye calibration')
    
    ## Step 2: Issue the command
    # PROMPT_BACKUP = 'Please move the green block onto my hand' # Default command
    
    # if input_way == 'keyboard':
    #     PROMPT = input('Step 2: Enter the command')
    #     if PROMPT == '':
    #         PROMPT = PROMPT_BACKUP
    # elif input_way == 'speech':
    #     record() # Start recording
    #     PROMPT = speech_recognition() # Voice recognition
    print('Step 2, the given command is:', PROMPT)
    
    ## Step 3: Capture a top-down image
    print('Step 3: Capturing a top-down image')
    top_view_shot(check=False)
    
    ## Step 4: Input the image to the multimodal vision model
    print('Step 4: Inputting the image to the multimodal vision model')
    img_path = 'temp/vl_now.jpg'
    
    n = 1
    while n < 5:
        try:
            print('    Attempting to call the multimodal vision model, attempt number:', n)
            result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg')
            print('    Successfully called the multimodal vision model!')
            print(result)
            break
        except Exception as e:
            print('    Error in response from the multimodal vision model, retrying...', e)
            n += 1
    
    ## Step 5: Post-processing and visualization of the model output
    print('Step 5: Post-processing and visualizing the output from the vision model')
    START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=True)
    
    ## Step 6: Hand-eye calibration transformation to robotic arm coordinates
    print('Step 6: Hand-eye calibration, converting pixel coordinates to robotic arm coordinates')
    # Start point in robotic arm coordinates
    START_X_MC, START_Y_MC = eye2hand(START_X_CENTER, START_Y_CENTER)
    # End point in robotic arm coordinates
    END_X_MC, END_Y_MC = eye2hand(END_X_CENTER, END_Y_CENTER)
    
    ## Step 7: Gripper picks up and moves the object
    print('Step 7: Gripper picks up and moves the object')
    pump_move(mc=mc, XY_START=[START_X_MC, START_Y_MC], XY_END=[END_X_MC, END_Y_MC])
    
    ## Step 8: Cleanup
    print('Step 8: Task completed')
    GPIO.cleanup()            # Release GPIO pin channels
    cv2.destroyAllWindows()   # Close all OpenCV windows
    # exit()