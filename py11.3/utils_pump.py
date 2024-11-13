# utils_pump.py
# Functions related to GPIO pins and mechanical gripper control

print('Importing mechanical gripper control module')
import time
import math
import smbus2 as smbus

class PCA9685:

    def __init__(self, address=0x40, debug=False):
        self.bus = smbus.SMBus(1)  # I2C bus 1
        self.address = address
        self.debug = debug
        self.write(0x00, 0x00)  # Initialize PCA9685
  
    def write(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)
    
    def setPWMFreq(self, freq):
        prescaleval = 25000000.0
        prescaleval /= 4096.0
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = math.floor(prescaleval + 0.5)

        oldmode = self.bus.read_byte_data(self.address, 0x00)
        newmode = (oldmode & 0x7F) | 0x10
        self.write(0x00, newmode)
        self.write(0xFE, int(prescale))
        self.write(0x00, oldmode)
        time.sleep(0.005)
        self.write(0x00, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        self.write(0x06 + 4 * channel, on & 0xFF)
        self.write(0x07 + 4 * channel, on >> 8)
        self.write(0x08 + 4 * channel, off & 0xFF)
        self.write(0x09 + 4 * channel, off >> 8)
    
    def setServoPulse(self, channel, pulse):
        pulse = pulse * 4096 / 20000  # Convert pulse to a 12-bit value
        self.setPWM(channel, 0, int(pulse))

# Functions for controlling the gripper
def clamp_close(pwm):
    '''
    Close the gripper to hold an object
    '''
    print('Gripper is closing to hold the object')
    pwm.setServoPulse(5, 2100)  # Set PWM to 2100, closing the gripper
    time.sleep(1)  # Wait for the action to complete

def clamp_open(pwm):
    '''
    Open the gripper to release the object
    '''
    print('Gripper is opening to release the object')
    pwm.setServoPulse(5, 1500)  # Set PWM to 1500, opening the gripper
    time.sleep(1)  # Wait for the action to complete

# Control for the 6th servo of the robotic arm
if __name__ == '__main__':
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)  # Set PWM frequency to 50Hz

    try:
        while True:
            command = input("Enter 'c' to close the gripper, 'o' to open, 'q' to quit: ")
            if command == 'c':
                clamp_close(pwm)
            elif command == 'o':
                clamp_open(pwm)
            elif command == 'q':
                print("Program terminated")
                break
            else:
                print("Invalid input")
    except KeyboardInterrupt:
        print("Program interrupted, stopping servos")