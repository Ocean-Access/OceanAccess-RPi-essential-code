from __future__ import print_function
import RPi.GPIO as IO
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)

def change_motor_speed(motor, speed):
    #must take two arrays, both should be of size 2
    #first array contains either 0 or 1, to indicate if the motor speed should be changed
    #second array is a number from -100 to +100, which indicates direction and %speed
    print(speed)
    if (len(motor)!= 2 or len(speed) != 2):
        print("This function must take two arrays, both should be of size 2")
        print("first array contains either 0 or 1, to indicate if the motor speed should be changed")
        print("second array is a number from -100 to +100, which indicates direction and %speed")
        return
    if (motor[0]):
        motors.motor1.setSpeed(speed[0]*0.01*MAX_SPEED)
        raiseIfFault()
    if (motor[1]):
        motors.motor2.setSpeed(speed[1]*0.01*MAX_SPEED)
        raiseIfFault()
    
def Reverse(reverse):
    IO.setmode(IO.BCM)
    IO.setup(17,IO.OUT)
    if reverse:
        IO.output(17,IO.LOW)
    else:
        IO.output(17,IO.HIGH)
    return

def alt_main():
    motors.enable()
    print("starting in 5s - sign altmain")
    time.sleep(5)
    
    #setting speed
    

    try:
        print("we at moto huan")
        Reverse(1)
        change_motor_speed([1,0],[100,0])#endre tall her
        change_motor_speed([0,1],[0,100]) #opening valve
        time.sleep(60)
        print("reversing soon!")
        time.sleep(10)
        change_motor_speed([0,1],[0,0]) #closing valve
        time.sleep(4)
        change_motor_speed([1,0],[0,0]) #turn off pump
        raiseIfFault()
    except DriverFault as e:
        print("Driver %s fault!" % e.driver_num)
    #finally:
    #    print("we did sumsum")
        # Stop the motors, even if there is an exception
        # or the user presses Ctrl+C to kill the process.
    #    motors.forceStop()
    #waiting
    
    time.sleep(60) #endre tall her #170 sekunder skal bli full tank på 4L
    
    change_motor_speed([0,1],[0,0]) #closing valve
    #time.sleep(3)
    change_motor_speed([1,0],[0,0]) #stopping pump
    
    
    #setting speed = 0%
    try:
        change_motor_speed([1,1],[0,0]) #stopp motor og lukk ventil
        raiseIfFault()
    
    
    except DriverFault as e:
        print("Driver %s fault!" % e.driver_num)
        
    
    
    motors.disable()



def main(enable_motors):
    IO.cleanup()
    print("hello world")
    if enable_motors:
        try:
            start=time.time()
            alt_main()
        finally:
            motors.forceStop()
            print(time.time()-start)
        return
    IO.setmode(IO.BCM) #setting up IE
    IO.setup(18,IO.OUT) # IE
    pwm = IO.PWM(18, 50000) #pin 18, aka pin 12 IE
    pwm.start(0)#starting the PWM with 0 power IE
    print("starting in 10s")
    time.sleep(10)	
    print("starting pump") 
    pwm.ChangeDutyCycle(99) # Fredrik sett tallet her mellom 0 og 100 
    time.sleep(60) #kjore i 300 s før den skrur sae av
    pwm.ChangeDutyCycle(0)
    pwm.stop() #IE
    IO.cleanup()
    
    

    return

if __name__ == main:
    main()
main(1)
