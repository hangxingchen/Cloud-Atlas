# utils_vlm.py
# Multimodal Large Model, Visualization

print('Importing vision large model module')
import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw

# Import English font, specify font size
font = ImageFont.truetype('asset/Arial.ttf', 26)

from API_KEY import *

# System prompt
SYSTEM_PROMPT = '''
I am about to give an instruction to the robotic arm. Please help me extract the start object and the end object from this instruction, 
and find the top-left and bottom-right pixel coordinates of these objects in the image. Output the result in JSON format.

For example, if my instruction is: "Please place the red block on the house sketch."
You should respond in this format:
{
 "start":"red block",
 "start_xyxy":[[102,505],[324,860]],
 "end":"house sketch",
 "end_xyxy":[[300,150],[476,310]]
}

Only respond with the JSON, do not include any other content.

Here is my instruction:
'''

# Yi-Vision API call function
import openai
from openai import OpenAI
import base64
def yi_vision_api(PROMPT='Place the red block on the pen', img_path='temp/vl_now.jpg'):

    '''
    Yi-Vision multimodal large model API
    '''

    client = OpenAI(
        api_key=YI_KEY,
        base_url="https://api.lingyiwanwu.com/v1"
    )

    # Encode the image as big5 traditional data
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('base64')




    # Send request to the large model
    completion = client.chat.completions.create(
      model="yi-vision",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": SYSTEM_PROMPT + PROMPT
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )

    # Parse the result from the large model
    result = eval(completion.choices[0].message.content.strip())
    print('    Large model call successful!')

    return result

def post_processing_viz(result, img_path, check=False):

    '''
    Post-processing and visualization of the vision model output
    check: Whether to manually confirm the visualization on the screen, press key to continue or exit
    '''

    # Post-processing
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]
    # Scaling factor
    FACTOR = 999
    # Start object name
    START_NAME = result['start']
    # End object name
    END_NAME = result['end']
    # Start object, top-left pixel coordinates
    START_X_MIN = int(result['start_xyxy'][0][0] * img_w / FACTOR)
    START_Y_MIN = int(result['start_xyxy'][0][1] * img_h / FACTOR)
    # Start object, bottom-right pixel coordinates
    START_X_MAX = int(result['start_xyxy'][1][0] * img_w / FACTOR)
    START_Y_MAX = int(result['start_xyxy'][1][1] * img_h / FACTOR)
    # Start object, center pixel coordinates
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # End object, top-left pixel coordinates
    END_X_MIN = int(result['end_xyxy'][0][0] * img_w / FACTOR)
    END_Y_MIN = int(result['end_xyxy'][0][1] * img_h / FACTOR)
    # End object, bottom-right pixel coordinates
    END_X_MAX = int(result['end_xyxy'][1][0] * img_w / FACTOR)
    END_Y_MAX = int(result['end_xyxy'][1][1] * img_h / FACTOR)
    # End object, center pixel coordinates
    END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)

    # Visualization
    # Draw start object box
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # Draw start object center point
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # Draw end object box
    img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # Draw end object center point
    img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
    # Write object names in English
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR to RGB
    img_pil = Image.fromarray(img_rgb) # Array to PIL image
    draw = ImageDraw.Draw(img_pil)
    # Write start object name in English
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # Text coordinates, English string, font, rgba color
    # Write end object name in English
    draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # Text coordinates, English string, font, rgba color
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB to BGR
    # Save the visualization image
    cv2.imwrite('temp/vl_now_viz.jpg', img_bgr)

    formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # Display the visualization on the screen
    cv2.imshow('zihao_vlm', img_bgr)

    if check:
        print('    Please confirm successful visualization, press "c" to continue or "q" to exit')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # Press "c" to continue
                break
            if key == ord('q'): # Press "q" to exit
                cv2.destroyAllWindows()   # Close all OpenCV windows
                raise NameError('Exited by pressing "q"')
    else:
        if cv2.waitKey(1) & 0xFF == None:
            pass

    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER
