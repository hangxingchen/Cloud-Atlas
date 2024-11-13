# agent_go.py
# Robotic Arm + LLM + Multimodal + Speech Recognition = Embodied Intelligent Agent

print('\nCloud Atlas')
print('HANG 2024-10-27 \n')

# Import common utility functions
from utils_asr import *             # Recording + Speech Recognition
from utils_robot import *           # Connect to robotic arm
from utils_llm import *             # Large Language Model API
from utils_camera import *          # Camera
from utils_robot import *           # Robotic arm movement
from utils_pump import *            # GPIO, Pump
from utils_vlm_move import *        # Multimodal model for image recognition and object manipulation
from utils_drag_teaching import *   # Drag Teaching
from utils_agent import *           # Agent Planning
from utils_tts import *             # Text-to-Speech module

# Play welcome message
pump_off()
# back_zero()
play_wav('asset/welcome.wav')


def agent_play():
    '''
    Main function to control the robotic arm using voice commands
    '''
    # Reset to initial position
    back_zero()
    
    # Get user input
    # Example: Reset to the initial position, then place the green block on the red block
    start_record_ok = input('Start recording，Enter a number for recording duration, press k for manual input, or press c for default command\n')
    if str.isnumeric(start_record_ok):
        DURATION = int(start_record_ok)
        record(DURATION=DURATION)   # Start recording
        order = speech_recognition() # Perform speech recognition
    elif start_record_ok == 'k':
        order = input('Please enter the command: ')
    elif start_record_ok == 'c':
        order = 'Reset, then shake head, and place the green block on the red block'
    else:
        print('No command given, exiting')
        raise NameError('No command given, exiting')
    
    # Agent planning
    agent_plan_output = eval(agent_plan(order))
    
    print('Agent planned actions:\n', agent_plan_output)
    # plan_ok = input('Continue? Press c to continue or q to quit')
    plan_ok = 'c'
    if plan_ok == 'c':
        response = agent_plan_output['response'] # Get the response from the robot
        print('Starting text-to-speech synthesis')
        tts(response)                     # Text-to-speech synthesis, export to wav file
        play_wav('temp/tts.wav')          # Play the synthesized audio file
        for each in agent_plan_output['function']: # Execute each function planned by the agent
            print('Executing action:', each)
            eval(each)
    elif plan_ok == 'q':
        raise NameError('Exited by user request')

# Run the main function if the script is executed directly
if __name__ == '__main__':
    agent_play()
