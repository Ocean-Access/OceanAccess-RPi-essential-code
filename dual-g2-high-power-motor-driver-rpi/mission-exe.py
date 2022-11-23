from __future__ import print_function
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
from pyudev import Context, Devices
import serial
from brping import Ping1D
import math
import time
import sys
import os
sys.path.append("/home/pi/ping-python/kellerLD")
from kellerLD import KellerLD
import argparse
import calendar
from builtins import input

class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)
#def AssignUSB(device_port):
#    context=Context()
#    device=Devices.from_device_file(context,'/dev/ttyUSB0')
#    print(device)
    #for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
    #    print(device) 
    

def Accelerometer(runtime,directory):
    #Need to use Frequency for something later, so this is workaround
    frequency=6.25
    FrequencySetting='FREQ ' + str(frequency)
    FrequencySetting=bytes(FrequencySetting,'ascii')
    
    #need num_samples for write to file
    num_samples=math.ceil(runtime*frequency)
    
    #INIT
    port = '/dev/ttyACM0'
    num_readings=math.ceil(runtime*frequency)
    usbacc = serial.Serial(port)
    usbacc.write(b'RANGE 2')
    usbacc.write(FrequencySetting)
    filename=os.path.join(directory,"accel_data.txt")
    file=open(filename,'a')
    file.write("sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    usbacc.write(b'START')
    for _ in range(num_readings):
        file.write(str(usbacc.readline()))
    
    #finish
    usbacc.write(b'STOP')
    usbacc.close()
    file.close()
    
    
def BlueRoboticsSonar(runtime,directory):
    #init
    myPing = Ping1D()
    myPing.connect_serial("/dev/ttyUSB_BRS", 115200)
    filename=os.path.join(directory,"BlueRoboticsSonar.txt")
    file=open(filename,'a')
    file.write("sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    
    time_run=0
    while (time_run<runtime):
        data = myPing.get_distance()
        if data:
            file.write("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
        else:
            file.write("Distance: NONE \tConfidence: NONE")
        time.sleep(0.04)
        time_run+=0.1
    file.close()

def BlueRoboticsPressureSensor(runtime,directory):
    sensor = KellerLD()
    sensor.init()tim
    filename=os.path.join(directory,"BlueRoboticsPressure.txt")
    file=open(filename,'a')
    file.write("sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    timer=0
    while (timer<runtime):
        sensor.read()
        file.write(str(sensor.pressure()))
        file.write(",")
        time.sleep(0.1)
        timer+=0.1
    file.close()
    
def ISA500(runtime,directory):
    ser = serial.Serial ("/dev/ttyUSB_ISA500")    #Open named port 
    ser.baudrate = 9600#Set baud rate to 9600
    
    raiseIfFault() #check if the motor hat has gone to shit
    motors.motor1.setSpeed(MAX_SPEED)
    time.sleep(5)
    filename=os.path.join(directory,"ISA500.txt")
    file=open(filename,'a') #next three lines are to open a file and start writing to it
    file.write("sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    filename2=os.path.join(directory,"ISA500-ahrs.txt")
    file2=open(filename2,'a') #next three lines are to open a file and start writing to it
    file2.write("sampling started at :")
    file2.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    timer=0
    while (timer<runtime):
        #commandline="#p<CR>"
        ser.write(b'#p<CR>')                  #send command string 
        reading=ser.read(ser.inWaiting())               #read data in read buffer
        file.write(str(reading))
        ser.write(b'#o<CR>')
        reading2=ser.read(ser.inWaiting())
        file2.write(str(reading2))
        time.sleep(0.04)
        timer+=0.1
    ser.close()
    file.close()
    motors.motor1.setSpeed(0)   
    
def ISD4000(runtime, directory):
    ser = serial.Serial ("/dev/ttyUSB_IDD4000")    #Open named port 
    ser.baudrate = 9600#Set baud rate to 9600
    
    raiseIfFault() #check if the motor hat has gone to shit
    motors.motor2.setSpeed(MAX_SPEED)
    time.sleep(5)
    filename=os.path.join(directory,"ISD4000.txt")
    file=open(filename,'a') #next three lines are to open a file and start writing to it
    file.write("sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    filename2=os.path.join(directory,"ISD4000-ahrs.txt")
    file2=open(filename2,'a') #next three lines are to open a file and start writing to it
    file2.write("sampling started at :")
    file2.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    timer=0
    while (timer<runtime):
        #commandline="#p<CR>"
        ser.write(b'#d<CR>')                  #send command string 
        reading=ser.read(ser.inWaiting())               #read data in read buffer
        file.write(str(reading))
        ser.write(b'#o<CR>')
        reading2=ser.read(ser.inWaiting())
        file2.write(str(reading2))
        time.sleep(0.1)
        timer+=0.1
    ser.close()
    file.close()
    file2.close()
    motors.motor2.setSpeed(0)   

def FindDirectory(date,reading):
    parentDirectory="/home/pi/ping-python/examples/"
    date_path=os.path.join(parentDirectory,date)
    if not os.path.exists(date_path):
        os.mkdir(date_path)
    reading_path=os.path.join(date_path,str(reading))
    if not os.path.exists(reading_path):
        os.mkdir(reading_path)
    return reading_path

def ShutDownIf(start_time,days):
    #turns the RPi off if the time difference between start_time and when the function is called is greater than 'days' number of days
    shutdown_condition=((time.time() - calendar.timegm(start_time)) > (days*24*60*60) )
    if (shutdown_condition):
        os.system('sudo shutdown')
def ErrorHandler(directory, sensor):
    filename=os.path.join(directory,"error.txt")
    file=open(filename,'a')
    file.write("Error when trying to handle: ")
    file.write(sensor)
    file.write("     /      ")
    file.close()
        

def Mission():
    #init
    runtime=600#in seconds, how long each sensor should read data
    samplings_per_day=8
    num_sensors=5
    sleeptime=((24*60*60)/samplings_per_day)-(runtime*num_sensors)
    A=True
    reading_num=1
    print("sleepin")
    time.sleep(3600)#gives us 20 minutes from we plug the batteries to when things start
    date=time.strftime("%A- %Y - %m - %d", time.gmtime())
    start_date=date
    while(A):
        ShutDownIf(start_date,12) # fist input is when the deployment started, second number is how long we want to run before shutting down (number is in days)
        #date=time.strftime("%A- %Y - %m - %d", time.gmtime())
        print(date)
        directory=FindDirectory(date,reading_num)
        
        try:
            ISA500(runtime,directory)
        except:
            ErrorHandler(directory,"ISA500")
        try:
            ISD4000(runtime,directory)
        except:
            ErrorHandler(directory,"ISD4000")
        try:
            BlueRoboticsSonar(runtime,directory)
        except:
            ErrorHandler(directory,"Blue Robotics Sonar")
        try:
            BlueRoboticsPressureSensor(runtime,directory)
        except:
            ErrorHandler(directory,"Blue Robotics Pressure Sensor")
        try:
            Accelerometer(runtime,directory)
        except:
            ErrorHandler(directory,"Accelerometer")
                
        #ISA500(runtime,directory)
        #ISD4000(runtime,directory)
    
        #BlueRoboticsSonar(runtime,directory)
        #BlueRoboticsPressureSensor(runtime,directory)
        #Accelerometer(runtime,directory)
        
        #dont want to do multiple readings while testing on land
        
        time.sleep(sleeptime)
        if reading_num==samplings_per_day:
            date=time.strftime("%A- %Y - %m - %d", time.gmtime())
            reading_num=0
            
        reading_num+=1
#print("started")  
#Mission()
Accelerometer(20, '/home/pi/ping-python/examples/')      
                
            
        
    