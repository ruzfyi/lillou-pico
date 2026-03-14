from machine import Pin, PWM, ADC
import time
import math
import sys
import select


poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

min_duty = 1638
max_duty = 8192


# comms setup
def get_command(command, ack):
    waiting = True
    while waiting:
        if poll_obj.poll(0):
            pi_command = sys.stdin.readline().rstrip()

            if pi_command == "RESET":
                print("ACK: SOFT RESETTING")
                machine.soft_reset()
            
            if pi_command == command:
                print("ACK:", ack)
                return True
           

#receive = get_command("PI_READY", "PICO_READY")

# drone servo
drone_pin = machine.Pin(18)
drone = machine.PWM(drone_pin)
drone.freq(50)

drone_launch = Pin(17, Pin.OUT)
drone_launch.value(0)

def toggle_drone():
    drone_launch.value(0)
    drone_launch.value(1)

# minibot release servo
release_pin = machine.Pin(15)
release = PWM(release_pin)
release.freq(50)

# sweeper servo
sweeper_pin = machine.Pin(13)
sweeper = PWM(sweeper_pin)
sweeper.freq(50)

# camera release servo
cam_release_pin = machine.Pin(8)
cam_release = machine.PWM(cam_release_pin)
release.freq(50)

# #minibot servo set up
# minibot_pin = machine.Pin(14)
# minibot = machine.PWM(minibot_pin)
# minibot.freq(50)
# 
# #sweep servo set up
# sweep_pin = machine.Pin(14)
# # sweep.freq(50)


# Sets angles for 270 degree servos
# def sweep_angle(angle):
#     # convert angle (0-270) to duty cycle
#     min_duty = 1638   # ~0.5ms
#     max_duty = 8192   # ~2.5ms
#     
#     duty = int(min_duty + (angle / 270) * (max_duty - min_duty))
#     sweep.duty_u16(duty)

#360 crank servo variables
STOP = 4915
FULL_FORWARD = 6554
FULL_REVERSE = 3277

m1_in1 = 7
m1_in2 = 22
m1_en = 6

m2_in1 = 10
m2_in2 = 9
m2_en = 11

m3_in1 = 1 
m3_in2 = 2
m3_en = 0 

m4_in1 = 3
m4_in2 = 4
m4_en = 5

#Pin configuration

m1_in1 = Pin(m1_in1, Pin.OUT)
m1_in2 = Pin(m1_in2, Pin.OUT)
m1_en = Pin(m1_en, Pin.OUT)

m2_in1 = Pin(m2_in1, Pin.OUT)
m2_in2 = Pin(m2_in2, Pin.OUT)
m2_en = Pin(m2_en, Pin.OUT)

m3_in1 = Pin(m3_in1, Pin.OUT)
m3_in2 = Pin(m3_in2, Pin.OUT)
m3_en = Pin(m3_en, Pin.OUT)

m4_in1 = Pin(m4_in1, Pin.OUT)
m4_in2 = Pin(m4_in2, Pin.OUT)
m4_en = Pin(m4_en, Pin.OUT)

#Setting PWM frequency
pwm_m1_en = PWM(m1_en)
pwm_m2_en = PWM(m2_en)
pwm_m3_en = PWM(m3_en)
pwm_m4_en = PWM(m4_en)

pwm_m1_en.freq(500)     # 10 kHz
pwm_m1_en.duty_u16(16384) #50% for (range: 0–65535)
pwm_m2_en.freq(500)     # 10 kHz
pwm_m2_en.duty_u16(16384) #50% for (range: 0–65535)
pwm_m3_en.freq(500)     # 10 kHz
pwm_m3_en.duty_u16(16384) #50% for (range: 0–65535)
pwm_m4_en.freq(500)     # 10 kHz
pwm_m4_en.duty_u16(16384) #50% for (range: 0–65535)
#32768 40% 
#36000 60%
#16384 25%

def stop_motors():
    m1_in1.value(0)
    m1_in2.value(0)
    m2_in1.value(0)
    m2_in2.value(0)
    m3_in1.value(0)
    m3_in2.value(0)
    m4_in1.value(0)
    m4_in2.value(0)

def wheel_test():
    #top_left wheel
    print("Wheel 1")
    m1_in1.value(1)
    m1_in2.value(0)
    time.sleep(2)
    m1_in1.value(0)
    m1_in2.value(0)
    
    #top right wheel
    print("Wheel 2")
    m2_in1.value(1)
    m2_in2.value(0)
    time.sleep(2)
    m2_in1.value(1)
    m2_in2.value(0)
    
    #bottom left wheel
    print("Wheel 3")
    m3_in1.value(1)
    m3_in2.value(0)
    time.sleep(2)
    m3_in1.value(0)
    m3_in2.value(0)
    
    #bottom right wheel
    print("Wheel 4")
    m4_in1.value(1)
    m4_in2.value(0)
    time.sleep(2)
    m4_in1.value(0)
    m4_in2.value(0)
    

def right_rotation(duration):
    
    # Seems like 1050-1075 is good time to rotate 90 degrees
    m1_in1.value(1)
    m1_in2.value(0)
    
    m2_in1.value(0)
    m2_in2.value(1)
    
    m3_in1.value(1)
    m3_in2.value(0)

    m4_in1.value(0)
    m4_in2.value(1)
    
    time.sleep_ms(duration)
    stop_motors()

def left_rotation(duration):
    
    # Seems like 1050-1075 is good time to rotate 90 degrees
    m1_in1.value(0)
    m1_in2.value(1)
    
    m2_in1.value(1)
    m2_in2.value(0)
    
    m3_in1.value(0)
    m3_in2.value(1)

    m4_in1.value(1)
    m4_in2.value(0)
    
    time.sleep_ms(duration)
    stop_motors()

#Time base functions
def forward_ms(duration_ms):
    # 1 second or 1000ms is around 13 inches (With good batteries)
    
    m1_in1.value(1)
    m1_in2.value(0)
    
    m2_in1.value(1)
    m2_in2.value(0)
    
    m3_in1.value(1)
    m3_in2.value(0)
    
    m4_in1.value(1)
    m4_in2.value(0)

    time.sleep_ms(duration_ms)
    stop_motors()
    

def backwards_ms(duration_ms):
    
    m1_in1.value(0)
    m1_in2.value(1)
    
    m2_in1.value(0)
    m2_in2.value(1)
    
    
    m3_in1.value(0)
    m3_in2.value(1)
    
    m4_in1.value(0)
    m4_in2.value(1)
    
    time.sleep_ms(duration_ms)
    stop_motors()
    
def right_ms(duration_ms):
    
    m1_in1.value(1)
    m1_in2.value(0)
    
    m2_in1.value(0)
    m2_in2.value(1)
    
    m3_in1.value(0)
    m3_in2.value(1)

    m4_in1.value(1)
    m4_in2.value(0)
    
    time.sleep_ms(duration_ms)
    stop_motors()
    
    
def left_ms(duration_ms):
    
    m1_in1.value(0)
    m1_in2.value(1)
    
    m2_in1.value(1)
    m2_in2.value(0)
    
    m3_in1.value(1)
    m3_in2.value(0)

    m4_in1.value(0)
    m4_in2.value(1)
    
    time.sleep_ms(duration_ms)
    stop_motors()

# drone control
def set_drone_angle(angle):
    duty = min_duty + int((angle/180) * (max_duty - min_duty))
    drone.duty_u16(duty)

def drone_reset():
    set_drone_angle(45)

def drone_move():
    set_drone_angle(0)

# camera release control
def set_camera_release_angle(angle):
    duty = min_duty + int((angle/180) * (max_duty - min_duty))
    cam_release.duty_u16(duty)

def release_camera():
    set_camera_release_angle(150)

def release_camera_reset():
    set_camera_release_angle(90)

# sweeper control
def set_sweeper_angle(angle):
    duty = min_duty + int((angle/180) * (max_duty - min_duty))
    sweeper.duty_u16(duty)

def sweeper_out():
    set_sweeper_angle(120)

def sweeper_reset():
    set_sweeper_angle(90)

# minibot release control
def set_release_angle(angle):
    duty = min_duty + int((angle/180) * (max_duty - min_duty))
    release.duty_u16(duty)

# it should always be at 90 to start
def release_minibot():
    set_release_angle(150)
    time.sleep(3)

    set_release_angle(90)

def release_minibot_reset():
    set_release_angle(90)
    time.sleep(2)

# button tasks
def button_task():
    print("sending start signal to PI")
    print("START")
    print("Moving to button")
    #Press button 
    forward_ms(1250)
    time.sleep(1)
    left_ms(700)
    time.sleep(0.5)
    

    print("Realising minibot")
    release_minibot()
    toggle_drone()
    print("Minibot should be released")
    time.sleep(1)
    drone_move()
    
    print("Releasing camera")
    release_camera()
    print("Camera should be released")

    print("Continuing to button")

    forward_ms(1250)
    time.sleep(0.5)
    backwards_ms(500)
    time.sleep(0.5)
    left_ms(500)
    time.sleep(0.5)
    forward_ms(750)
    time.sleep(0.5)
    backwards_ms(500)
    time.sleep(0.5)
    left_ms(500)
    time.sleep(0.5)
    forward_ms(750)
    time.sleep(0.5)
    #Moving a bit back to set camera
    backwards_ms(500)
    time.sleep(0.5)
    right_rotation(1050)
    time.sleep(0.5)
    
    #READ COLOR
    #print("COLOR_1_READY")
    #receive = get_command("COLOR_1_DONE", "OK")

def correcting_pos():
    left_rotation(1050)
    time.sleep(0.5)
    backwards_ms(500)
    time.sleep(0.5)
    left_ms(500)
    time.sleep(0.5)

def button_to_crank():
    right_ms(1500)
    time.sleep(0.5)
    right_rotation(1000)
    time.sleep(0.5)
    #Looking torwards crater
    left_ms(2650)
    time.sleep(0.5)
    #Go straight and left to hug the wall
    forward_ms(2000)
    time.sleep(0.5)
    left_ms(1000)
    time.sleep(0.5)
    left_rotation(400)
    time.sleep(0.5)
    forward_ms(3500)
    time.sleep(0.5)
    backwards_ms(400)
    time.sleep(0.5)
    left_ms(1000)
    time.sleep(0.5)
    """
    right_ms(1000)
    time.sleep(0.5)
    right_rotation(1000)
    time.sleep(0.5)
    left_ms(1000)
    time.sleep(0.5)
    backwards_ms(1000)
    time.sleep(0.5)
    """
    
def position_crank():
    #Reached other side of the wall
    right_ms(1500)
    time.sleep(0.5)
    right_rotation(1070)
    time.sleep(0.5)
    left_ms(1500)
    time.sleep(0.5)
    backwards_ms(750)
    time.sleep(0.5)
    left_ms(100)
    time.sleep(0.5)
    
def crank_task():
    
    crank.duty_u16(FULL_FORWARD) 
    time.sleep(.5)
    #5700    
    crank.duty_u16(STOP)
    
    right_ms(250)
    
#     crank.duty_u16(FULL_FORWARD) 
#     time.sleep(1)
    
    crank.duty_u16(STOP)
    
    left_ms(250)
    
    crank.duty_u16(FULL_FORWARD)
    time.sleep(5)    
    
    crank.duty_u16(STOP)

def button_to_keypad():
    right_ms(2950)
    time.sleep(0.5)
    left_rotation(1150)
    time.sleep(0.5)
    left_ms(1500)
    time.sleep(0.5)

def keypad_task():
    print("AT_KEYPAD")
    receive = get_command("KEYPAD_DONE", "OK")

def keypad_to_home():
    forward_ms(2000)
    time.sleep(0.5)
    left_ms(1500)
    time.sleep(0.5)
    forward_ms(2000)
    time.sleep(0.5)

    
def to_pressure_plate():
    forward_ms(2000)
    time.sleep(.5)
        
    right_rotation(1250)
    time.sleep(.5)
    
    left_ms(1000)
    time.sleep(.5)    
    
    forward_ms(500)
    time.sleep(.5)   
    
    left_rotation(250)
    time.sleep(.5)    

# initial halt till PI requests us
receive = get_command("PI_READY", "OK")
                      
# testing sweep_out
# sweeper_out()
# time.sleep(1)

led = Pin(16, Pin.OUT)
led.off()

sweeper_reset()
print("sweeper reset")    

release_minibot_reset()
print("minibot release reset")

release_camera_reset()
print("camera release reset")

drone_reset()
print("drone servo reset")

print("prepping photoresistor")
photores_value = ADC(26) # GP26

value = photores_value.read_u16() # Reads 0-65535
print("photoresistor initialized")

#waiting for photoresistor threshold to be reached
print("STARTING UP")

while (value > 10000):
    value = photores_value.read_u16()
    print(value)
    time.sleep(0.2)
print("PHOTO_RESISTOR WORKED")

led.on()

#everything under here is the robot's logic (move forward, left, right and anything)

while True:
    
    button_task()
    
    stop_motors()

    print("COLOR_1_READY")
    
    response = get_command("COLOR_1_DONE", "OK")

    correcting_pos()
    
    button_to_keypad()

    stop_motors()

    keypad_task()

    keypad_to_home()

    stop_motors()

    print("LIST_COLORS")
    
    break
