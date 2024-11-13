# utils_robot.py
# Start and connect the robotic arm and import various toolkits
import time
import math
import smbus2 as smbus   #import smbus 
import cv2
import numpy as np
from utils_pump import *


# Initialize PCA9685 instance
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)  # Set PWM frequency to 50Hz

# Control the gripper
def control_gripper(action):
    if action == "open":
        pwm.setServoPulse(5, cal_pwm(90))  # Open the gripper
        print("Gripper opened")
    elif action == "close":
        pwm.setServoPulse(5, cal_pwm(144))  # Close the gripper
        print("Gripper closed")
    else:
        print("Invalid action command")


pca = PCA9685(0x40, debug=False)
pca.setPWMFreq(50)  # Set the PWM frequency to 50Hz





def set_servo_angle(channel, angle):
    # Set pulse width range and angle limit according to different servo channels
    if channel == 0:  # Servo 1, 0-180°, OUT0
        pulse = 500 + (angle / 180.0) * 2000
        pulse = max(500, min(2500, pulse))  # Limit the pulse width to 500-2500
    elif channel == 1:  # Servo 2, 0-270°, OUT1
        pulse = 500 + (angle / 270.0) * 2000
        pulse = max(500, min(2500, pulse))
    elif channel == 2:  # Servo 3, 0-270°, OUT2
        pulse = 550 + (angle / 270.0) * 1950
        pulse = max(550, min(2500, pulse))
    elif channel == 3:  # Servo 4, 0-270°, OUT3
        pulse = 500 + (angle / 270.0) * 2000
        pulse = max(500, min(2500, pulse))
    elif channel == 4:  # Servo 5, 0-180°, OUT4
        pulse = 500 + (angle / 180.0) * 2000
        pulse = max(500, min(2500, pulse))
    elif channel == 5:  # Servo 6, 0-180°, OUT5
        pulse = 1500 + (angle / 180.0) * 600
        pulse = max(1500, min(2100, pulse))  # Limit the pulse width to 1500-2100
    else:
        print("Invalid channel")
        return
    pca.setServoPulse(channel, pulse)  # Set the PWM pulse width for the corresponding channel
    print(f"Set servo on channel {channel} to angle {angle}°, with a pulse width of {pulse}")





# Configuration of servo angle and PWM limits My newly added physical limits of servo movement
servo_limits = {
    0: {"min_angle": 0, "max_angle": 180, "min_pulse": 500, "max_pulse": 2500},   # Servo 1
    1: {"min_angle": 0, "max_angle": 270, "min_pulse": 850, "max_pulse": 2300},   # Servo 2
    2: {"min_angle": 0, "max_angle": 270, "min_pulse": 550, "max_pulse": 2500},   # Servo 3
    3: {"min_angle": 0, "max_angle": 270, "min_pulse": 500, "max_pulse": 2500},   # Servo 4
    4: {"min_angle": 0, "max_angle": 180, "min_pulse": 500, "max_pulse": 2500},   # Servo 5
    5: {"min_angle": 0, "max_angle": 180, "min_pulse": 1500, "max_pulse": 2100}   # Servo 6
}





def set_servo_angle(channel, angle):
    if channel not in servo_limits:
        print("Invalid channel")
        return
    
    # Retrieve the servo limits for the current channel
    limits = servo_limits[channel]
    min_angle = limits["min_angle"]
    max_angle = limits["max_angle"]
    min_pulse = limits["min_pulse"]
    max_pulse = limits["max_pulse"]


    # Ensure the angle is within the allowed range
    if angle < min_angle or angle > max_angle:
        print(f"Angle out of range! The valid angle range for channel {channel} is {min_angle}° to {max_angle}°")
        return

    # Calculate the corresponding PWM pulse width
    pulse = min_pulse + (angle - min_angle) * (max_pulse - min_pulse) / (max_angle - min_angle)
    pulse = max(min_pulse, min(max_pulse, pulse))  # Limit the pulse width to the allowed range

    pca.setServoPulse(channel, pulse)  # Set the PWM pulse width for the corresponding channel
    print(f"Set servo on channel {channel} to angle {angle}°, with a pulse width of {pulse}")






def back_zero():
    '''
    Move the robotic arm back to the zero position with specified PWM pulse widths
    '''
    print('Moving the robotic arm to the zero position')
    pwm_values = [1500, 1500, 1500, 1500, 1610, 1500]  # Specified PWM pulse widths

    for i, pwm in enumerate(pwm_values):
        pca.setServoPulse(i, pwm)  # Set the PWM pulse width for the corresponding channel
        print(f'Set PWM pulse width for channel {i} to {pwm}')

    time.sleep(3)  # Pause for 3 seconds to ensure the arm completes the movement


def relax_arms():
    '''
    Relax the joints of the robotic arm to specified PWM pulse widths
    '''
    print('Relaxing the joints of the robotic arm')
    pwm_values = [1500, 1200, 550, 1200, 1610, 1400]  # Specified PWM pulse widths

    for i, pwm in enumerate(pwm_values):
        pca.setServoPulse(i, pwm)  # Set the PWM pulse width for the corresponding channel
        print(f'Set PWM pulse width for channel {i} to {pwm}')

    time.sleep(3)  # Pause for 3 seconds to ensure the arm completes the movement



def set_servo_pulses(pwm_values):
    """
    Set PWM pulse widths for all servos in a batch.
    Parameters:
    - pwm_values: A list containing 6 PWM pulse values, e.g., [1500, 1200, 550, 1200, 1610, 1400].
    """
    if len(pwm_values) != 6:
        print("Error: The pwm_values list must contain 6 values, one for each servo channel.")
        return

    for i, pwm in enumerate(pwm_values):
        pca.setServoPulse(i, pwm)
        print(f"Set PWM pulse width for channel {i} to {pwm}")







def head_shake():
    print('Shaking head left and right')  # Start head shaking
    set_servo_pulses([1500, 1200, 550, 1200, 1610, 1400])  # Center position
    time.sleep(1)  # Pause for 1 second

    # Shake left and right twice
    for _ in range(2):
        set_servo_pulses([1100, 1200, 550, 1200, 1610, 1400])  # Left position
        time.sleep(0.5)  # Pause for 0.5 seconds

        set_servo_pulses([1900, 1200, 550, 1200, 1610, 1400])  # Right position
        time.sleep(0.5)  # Pause for 0.5 seconds

    set_servo_pulses([1500, 1200, 550, 1200, 1610, 1400])  # Return to center position
    time.sleep(1)  # Pause for 1 second

if __name__ == '__main__':
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)  # Set PWM frequency to 50Hz

    try:
        # Execute head shaking
        head_shake()
    
    except KeyboardInterrupt:
        print("Program interrupted, stopping servo motors")


def head_dance():
    # Dance movement
    print('Robotic arm dancing')
    set_servo_pulses([1300, 1200, 550, 1200, 1610, 1400])  # Center position
    time.sleep(1)
    set_servo_pulses([1700, 1200, 550, 1000, 1610, 2100])  # Move down
    time.sleep(0.5)
    set_servo_pulses([1300, 1200, 550, 1400, 1610, 1400])  # Move up
    time.sleep(0.5)
    set_servo_pulses([1400, 1200, 550, 1000, 1610, 2100])  # Move down
    time.sleep(0.5)
    set_servo_pulses([1700, 1200, 550, 1400, 1610, 1400])  # Move up
    time.sleep(0.5)
    set_servo_pulses([1800, 1200, 550, 1200, 1610, 1400])  # Return to center position
    time.sleep(1)


def head_nod():
    # Nod movement
    print('Robotic arm nodding')
    set_servo_pulses([1500, 1200, 550, 1200, 1610, 1400])  # Center position
    time.sleep(1)
    set_servo_pulses([1500, 1200, 550, 1000, 1610, 2100])  # Move down (nod down)
    time.sleep(0.5)
    set_servo_pulses([1500, 1200, 550, 1400, 1610, 1400])  # Move up (nod up)
    time.sleep(0.5)
    set_servo_pulses([1500, 1200, 550, 1000, 1610, 2100])  # Move down (nod down)
    time.sleep(0.5)
    set_servo_pulses([1500, 1200, 550, 1400, 1610, 1400])  # Move up (nod up)
    time.sleep(0.5)
    set_servo_pulses([1500, 1200, 550, 1200, 1610, 1400])  # Return to center position
    time.sleep(1)




def move_to_coords(X=150, Y=-130, HEIGHT_SAFE=230):
    print('移动至指定坐标：X {} Y {}'.format(X, Y))
    # 这部分根据机械臂具体实现情况修改舵机角度来控制机械臂位置

def single_joint_move(joint_index, angle):
    print('关节 {} 旋转至 {} 度'.format(joint_index, angle))
    set_servo_angle(joint_index, angle)
    time.sleep(2)


def move_to_top_view(target_pwm_values=[1500, 1450, 1000, 600, 1610, 1400]):
    """
    Move the robotic arm to a top-view position, simulating servo movement speed.
    target_pwm_values: List of target PWM values, e.g., [1500, 1450, 1000, 600, 1610, 1400]
    """
    print('Moving to top-view position')
    
    # Initialize or update current PWM values
    global current_pwm_values
    if current_pwm_values is None:
        current_pwm_values = [1500] * len(target_pwm_values)

    # Gradually move PWM values from current to target
    for step in range(0, 101, 10):
        for i, target_pwm in enumerate(target_pwm_values):
            current_pwm = current_pwm_values[i] + (target_pwm - current_pwm_values[i]) * (step / 100.0)
            current_pwm = max(500, min(2500, int(current_pwm)))  # Limit PWM values
            pca.setServoPulse(i, current_pwm)
            print(f'Set PWM pulse width for channel {i} to {current_pwm}')
        
        # Short delay for smooth movement
        time.sleep(0.005)

    # Ensure stability after movement
    time.sleep(1)



def top_view_shot(check=False):
    """
    Capture a top-view image and save it.
    check: Whether to manually confirm if the image capture was successful.
    """
    print('Moving to top-view position')
    move_to_top_view()
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open the camera. Please check the camera connection.")
        return

    time.sleep(0.3)  # Wait for the camera to initialize
    success, img_bgr = cap.read()
    
    if success:
        # Save the image with a timestamp to avoid overwriting
        file_name = f'temp/vl_now_{int(time.time())}.jpg'
        cv2.imwrite(file_name, img_bgr)
        print(f'Image saved to {file_name}')

        # Display the image
        cv2.imshow('HANG_vlm', img_bgr)
        
        # Manual confirmation if required
        if check:
            print('Please confirm the image. Press "c" to continue, "q" to quit.')
            while True:
                key = cv2.waitKey(10) & 0xFF
                if key == ord('c'):  # Continue
                    break
                elif key == ord('q'):  # Quit
                    print("Exiting as requested by the user.")
                    cv2.destroyAllWindows()
                    cap.release()
                    raise SystemExit('User exited the program.')

        # Wait for a key press to close the window
        cv2.waitKey(0)
    else:
        print("Failed to capture the image.")

    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()

    
   






import numpy as np

# Define the lengths of the robot arm links
l1 = 105  # Length of the first link
l2 = 265  # Length of the second link
l3 = 220  # Length of the third link
l4 = 145  # Length of the end link

# Function to convert image coordinates to robot arm coordinates
def eye2hand(X_im=160, Y_im=120):
    '''
    Convert the target point from image pixel coordinates to robot arm coordinates.
    '''
    cali_1_im = [0, 478]                       # Bottom-left corner, first calibration point (image coordinates)
    cali_1_mc = [-21.8, -197.4]                # Bottom-left corner, first calibration point (robot coordinates)
    cali_2_im = [640, 0]                       # Top-right corner, second calibration point (image coordinates)
    cali_2_mc = [215, -59.1]                   # Top-right corner, second calibration point (robot coordinates)
    
    X_cali_im = [cali_1_im[0], cali_2_im[0]]
    X_cali_mc = [cali_1_mc[0], cali_2_mc[0]]
    Y_cali_im = [cali_2_im[1], cali_1_im[1]]
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]

    # Perform linear interpolation to map image coordinates to robot coordinates
    X_mc = int(np.interp(X_im, X_cali_im, X_cali_mc))
    Y_mc = int(np.interp(Y_im, Y_cali_im, Y_cali_mc))

    return X_mc, Y_mc




# Inverse kinematics function
def inverse_kinematics(x, y, z, beta, type="lower"):
    """
    Given a target point (x, y, z) and the end-effector angle beta, calculate the joint angles.
    """
    beta = np.deg2rad(beta)  # Convert beta from degrees to radians
    theta_0 = np.arctan2(y, x)  # Calculate the base rotation angle
    theta_3 = beta  # Initialize the end-effector angle

    # Calculate temporary coordinates in the XZ plane
    x_tmp = x / np.cos(theta_0) - l4 * np.cos(theta_3)
    z_tmp = z - l1 - l4 * np.sin(theta_3)
    r = np.sqrt(x_tmp**2 + z_tmp**2)  # Distance from the adjusted point to the origin

    # Check if the target point is within the robot arm's reachable range
    max_reach = l2 + l3
    min_reach = abs(l2 - l3)
    if r > max_reach or r < min_reach:
        print("Target position is out of the robot arm's reachable range.")
        return None

    # Use the cosine law to calculate theta_2
    cos_theta2 = (r**2 - l2**2 - l3**2) / (2 * l2 * l3)
    cos_theta2 = np.clip(cos_theta2, -1, 1)  # Clip the value to avoid invalid input
    theta_2 = np.arccos(cos_theta2)
    
    if type == "upper":  # Choose between "upper" or "lower" elbow configuration
        theta_2 = -theta_2

    epsilon = np.arctan2(l3 * np.sin(theta_2), l2 + l3 * np.cos(theta_2))
    phi = np.arctan2(z_tmp, x_tmp)
    theta_1 = phi - epsilon
    theta_3 = theta_3 - theta_2 - theta_1  # Adjust the end-effector angle

    # Convert the results to degrees
    theta_0 = np.degrees(theta_0)
    theta_1 = np.degrees(theta_1)
    theta_2 = np.degrees(theta_2)
    theta_3 = np.degrees(theta_3)
    
    return theta_0, theta_1, theta_2, theta_3







def move_to_target(X_im, Y_im, Z=20, beta=45):
    """
    Given target image coordinates (X_im, Y_im), along with Z-axis height and end-effector angle beta,
    control the robotic arm to move to the specified target position.
    
    Parameters:
    - X_im (int/float): Target X-coordinate in the image (pixel).
    - Y_im (int/float): Target Y-coordinate in the image (pixel).
    - Z (int/float): Target height (default is 20).
    - beta (int/float): End-effector angle in degrees (default is 45).
    """
    try:
        # Convert image coordinates to robot arm physical coordinates
        X_mc, Y_mc = eye2hand(X_im, Y_im)
        print(f"Converted image coordinates ({X_im}, {Y_im}) to robot coordinates ({X_mc}, {Y_mc})")

        # Calculate joint angles using inverse kinematics
        joint_angles = inverse_kinematics(X_mc, Y_mc, Z, beta)

        # Check if valid joint angles were obtained
        if joint_angles is not None:
            theta_0, theta_1, theta_2, theta_3 = joint_angles
            print("Calculated joint angles for target position:")
            print(f"Base joint (theta_0): {theta_0:.2f}°")
            print(f"Shoulder joint (theta_1): {theta_1:.2f}°")
            print(f"Elbow joint (theta_2): {theta_2:.2f}°")
            print(f"Wrist joint (theta_3): {theta_3:.2f}°")

            # TODO: Add actual robotic arm control code here
            # Example: send calculated angles to the robotic arm controller
            send_to_arm(theta_0, theta_1, theta_2, theta_3)
            print("Successfully sent joint angles to the robotic arm.")
        else:
            print("Unable to reach the specified target position.")

    except Exception as e:
        print(f"Error during move_to_target execution: {e}")




# Gripper Control Function
def activate_gripper(state):
    """
    Function to control the gripper.
    state: True means close (grip), False means open (release).
    """
    if state:
        print("Gripper activated, gripping the object.")
        # Add the actual control code here, e.g., using a PWM signal to close the gripper.
    else:
        print("Gripper released, letting go of the object.")
        # Add the actual control code here, e.g., using a PWM signal to open the gripper.




# Function to grab and move an object
def pump_move(XY_START=[230, -50], HEIGHT_START=50, XY_END=[100, 220], HEIGHT_END=100, HEIGHT_SAFE=220, beta=45):
    """
    Use the gripper to grab an object from the starting point and move it to the endpoint.
    
    Parameters:
    - XY_START: Starting coordinates of the robotic arm (x, y)
    - HEIGHT_START: Starting height, e.g., use 90 for a block, 70 for a small box
    - XY_END: Ending coordinates of the robotic arm (x, y)
    - HEIGHT_END: Ending height
    - HEIGHT_SAFE: Safe height during transportation
    - beta: End-effector angle in degrees (default is 45)
    """

    # 1. Move to a safe height above the starting point
    print("Moving to a safe height above the starting point")
    move_to_target_with_pwm(XY_START[0], XY_START[1], HEIGHT_SAFE, beta)

    # 2. Lower down to the starting height and grab the object
    print("Lowering down to the starting height and preparing to grab the object")
    move_to_target_with_pwm(XY_START[0], XY_START[1], HEIGHT_START, beta)
    activate_gripper(True)  # Activate the gripper to grab the object

    # 3. Lift up to the safe height
    print("Grab complete, lifting up to the safe height")
    move_to_target_with_pwm(XY_START[0], XY_START[1], HEIGHT_SAFE, beta)

    # 4. Move to a safe height above the endpoint
    print("Moving to a safe height above the endpoint")
    move_to_target_with_pwm(XY_END[0], XY_END[1], HEIGHT_SAFE, beta)

    # 5. Lower down to the ending height and release the object
    print("Lowering down to the ending height and releasing the object")
    move_to_target_with_pwm(XY_END[0], XY_END[1], HEIGHT_END, beta)
    activate_gripper(False)  # Deactivate the gripper to release the object

    # 6. Return to the safe height
    print("Placement complete, returning to the safe height")
    move_to_target_with_pwm(XY_END[0], XY_END[1], HEIGHT_SAFE, beta)




