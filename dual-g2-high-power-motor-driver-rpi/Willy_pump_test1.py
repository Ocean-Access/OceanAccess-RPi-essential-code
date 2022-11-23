from __future__ import print_function
import RPi.GPIO as IO
import time, sys
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import threading
class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)

global count
global start_counter
start_counter=0
count = 0


def countPulse(channel):
   global count
   if start_counter == 1:
      count = count+1
      

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
    
    #print("starting in 5s - sign altmain")
    #time.sleep(5)
    global start_counter
    global count
    FLOW_SENSOR_GPIO = 16
    IO.setmode(IO.BCM)
    IO.setup(FLOW_SENSOR_GPIO,IO.IN,pull_up_down=IO.PUD_UP)
    
    IO.add_event_detect(FLOW_SENSOR_GPIO, IO.FALLING, callback=countPulse, bouncetime=1)
    #setting speed
    pumptime=240 #juster tid her
    #change_motor_speed([0,1],[0,100]) #opening valve
    #time.sleep(3)
    try:
        print("we at moto huan")
        Reverse(0) #Go in not-reverse #rev == into tank
        start_counter=1
        change_motor_speed([1,1],[100,100])
        time.sleep(pumptime)
        change_motor_speed([0,1],[0,0])
        time.sleep(3)#endre tall her
        change_motor_speed([1,0],[0,0])
        start_counter=0
        raiseIfFault()
        flow = (count / (22000*(pumptime/60))) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        print("The flow is: %.3f Liter/min" % (flow))
        print("The flow was %.3f Liters " % (count/22000))
    except DriverFault as e:
        print("Driver %s fault!" % e.driver_num)
    #finally:
    #    print("we did sumsum")
        # Stop the motors, even if there is an exception
        # or the user presses Ctrl+C to kill the process.
    #    motors.forceStop()
    #waiting
    
     #endre tall her #170 sekunder skal bli full tank på 4L
    
    change_motor_speed([0,1],[0,0]) #closing valve
    #time.sleep(3)
    change_motor_speed([1,0],[0,0]) #stopping pump
    
    
    #setting speed = 0%
    try:
        change_motor_speed([1,1],[0,0]) #stopp motor og lukk ventil
        raiseIfFault()
    
    
    except DriverFault as e:
        print("Driver %s fault!" % e.driver_num)
        
    
    
    #motors.disable()



def main(enable_motors):
    IO.cleanup()
    global count
    global start_counter
    print("hello world")
    #floow=threading.Thread(target=flow,args=())
    #puump=threading.Thread(target=alt_main,args=())
    if enable_motors:
        try:
            start=time.time()
            #floow.start()
            #puump.start()
            alt_main()
        finally:
            try:
                #floow.stop()
                #puump.stop()
                start_counter=0
                change_motor_speed([0,1],[0,0])
                time.sleep(3)
                change_motor_speed([1,0],[0,0])
                
            except:
                motors.forceStop()
            motors.forceStop()
            a=time.time()-start
            print(a)
            flow = (count / (22000*(a/60)))
            print("ONLY IF CTRL + C : The flow is: %.3f Liter/min" % (flow)) 
            print("The flow was %.3f Liters " % (flow*(a/60)) )
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
def bare_ventil():
    try:
        change_motor_speed([0,1],[0,100])
        time.sleep(200)
    finally:
        change_motor_speed([0,1],[0,0])


#if __name__ == main:
#    main()
main(1)
#bare_ventil()