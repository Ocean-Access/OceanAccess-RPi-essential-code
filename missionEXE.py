from __future__ import print_function
import time
import smbus
from dual_g2_hpmd_rpi import motors, MAX_SPEED
from pyudev import Context, Devices
import serial
from brping import Ping1D
import math
import time
import sys
import os
sys.path.append("/home/pi/ping-python/kellerLD")
try:
    from kellerLD import KellerLD
except:
    pass
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
def FindCorrectPort(examplecommand):
    try:
        ser = serial.Serial("/dev/ttyÙSB0")    #Open named port 
        ser.baudrate = 9600#Set baud rate to 9600
        ser.write(examplecommand)
        reading=ser.read(ser.inWaiting())
        if len(reading)<5:
            raise Exception("Wrong port")
        else:
            return "/dev/ttyUSB0"
            
    except:
        try:
            ser = serial.Serial ("/dev/ttyUSB0")    #Open named port 
            ser.baudrate = 9600#Set baud rate to 9600
            ser.write(examplecommand)
            reading=ser.read(ser.inWaiting())
            if len(reading)<5:
                raise Exception("Wrong port")
            else:
                return "/dev/ttyUSB0"
            
        except:
            try:
                ser = serial.Serial ("/dev/ttyUSB1")    #Open named port 
                ser.baudrate = 9600#Set baud rate to 9600
                ser.write(examplecommand)
                reading=ser.read(ser.inWaiting())
                if len(reading)<5:
                    raise Exception("Wrong port")
                else:
                    return "/dev/ttyUSB1"
            except:
                try:
                    ser = serial.Serial ("/dev/ttyUSB2")    #Open named port 
                    ser.baudrate = 9600#Set baud rate to 9600
                    ser.write(examplecommand)
                    reading=ser.read(ser.inWaiting())
                    if len(reading)<5:
                        raise Exception("Wrong port")
                    else:
                        return "/dev/ttyUSB2"
            
                except: 
                    try:
                        ser = serial.Serial ("/dev/ttyUSB3")    #Open named port 
                        ser.baudrate = 9600#Set baud rate to 9600
                        ser.write(examplecommand)
                        reading=ser.read(ser.inWaiting())
                        if len(reading)<5:
                            raise Exception("Wrong port")
                        else:
                            return "/dev/ttyUSB3"
                        
                    except:
                        try:
                            ser = serial.Serial ("/dev/ttyUSB4")    #Open named port 
                            ser.baudrate = 9600#Set baud rate to 9600
                            ser.write(examplecommand)
                            reading=ser.read(ser.inWaiting())
                            if len(reading)<5:
                                raise Exception("Wrong port")
                            else:
                                return "/dev/ttyUSB2"
                        except:
                            print(" \n Could not find a suitable port \n")
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
    try:
        myPing = Ping1D()
        myPing.connect_serial("/dev/ttyUSB_BRS", 115200)
    except:
        try:
            myPing = Ping1D()
            myPing.connect_serial("/dev/ttyUSB0", 115200)
        except:
            try:
                myPing = Ping1D()
                myPing.connect_serial("/dev/ttyUSB1", 115200)
            except:
                try:
                    myPing = Ping1D()
                    myPing.connect_serial("/dev/ttyUSB2", 115200)
                except: 
                    try:
                        myPing = Ping1D()
                        myPing.connect_serial("/dev/ttyUSB3", 115200)
                    except:
                        try:
                            myPing = Ping1D()
                            myPing.connect_serial("/dev/ttyUSB4", 115200)
                        except:
                            print(name," does not work \n")
    filename=os.path.join(directory,"BlueRoboticsSonar.txt")
    file=open(filename,'a')
    file.write("\n sampling started at :")
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
    sensor.init()
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
    
def ISA500(runtime,directory,port="/dev/ttyUSB_ISA500"):
    bus=smbus.SMBus(1)
    bus.write_i2c_block_data(0x18,0x10,[0x01]) #skal vaerer 0x01 på slutten
    name="ISA500"
    time.sleep(10)
    port=FindCorrectPort(b'#p\r')
    ser = serial.Serial(port)    #Open named port 
    ser.baudrate = 9600#Set baud rate to 9600
    raiseIfFault() #check if the motor hat has gone to shit
    #motors.motor1.setSpeed(MAX_SPEED)
    time.sleep(5)
    filename=os.path.join(directory,"ISA500.txt")
    file=open(filename,'a') #next three lines are to open a file and start writing to it
    file.write("\n sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    filename2=os.path.join(directory,"ISA500-ahrs.txt")
    file2=open(filename2,'a') #next three lines are to open a file and start writing to it
    file2.write("\n sampling started at :")
    file2.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    timer=0
    while (timer<runtime):
        #commandline="#p<CR>"
        ser.write(b'#p\r')                  #send command string 
        reading=ser.read(ser.inWaiting())               #read data in read buffer
        file.write(str(reading))
        ser.write(b'#o\r')
        reading2=ser.read(ser.inWaiting())
        file2.write(str(reading2))
        time.sleep(0.04)
        timer+=0.1
    ser.close()
    file.close()
    bus.write_i2c_block_data(0x18,0x10,[0x00])
    
def ISD4000(runtime, directory,port="/dev/ttyUSB_IDD"):
    bus=smbus.SMBus(1)
    bus.write_i2c_block_data(0x18,0x10,[0x02]) #sskal vaere 0x02 paa sluttne
    name="ISD4000"
    time.sleep(10)
    port=FindCorrectPort(b'#d\r')
    ser = serial.Serial(port)    #Open named port 
    ser.baudrate = 9600#Set baud rate to 9600

    raiseIfFault() #check if the motor hat has gone to shit
    motors.motor2.setSpeed(MAX_SPEED)
    #time.sleep(5)
    filename=os.path.join(directory,"ISD4000.txt")
    file=open(filename,'a') #next three lines are to open a file and start writing to it
    file.write("\nsampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    filename2=os.path.join(directory,"ISD4000-ahrs.txt")
    file2=open(filename2,'a') #next three lines are to open a file and start writing to it
    file2.write("\nsampling started at :")
    file2.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    timer=0
    while (timer<runtime):
        #commandline="#p<CR>"
        ser.write(b'#d\r')                  #send command string 
        reading=ser.read(ser.inWaiting())               #read data in read buffer
        file.write(str(reading))
        ser.write(b'#o\r')
        reading2=ser.read(ser.inWaiting())
        file2.write(str(reading2))
        time.sleep(0.1)
        timer+=0.1
    ser.close()
    file.close()
    file2.close()
    bus.write_i2c_block_data(0x18,0x10,[0x00])
    #motors.motor2.setSpeed(0)   

def FindDirectory(date,reading):
    parentDirectory="/home/pi/OceanAccess-RPi-essential-code/"
    date_path=os.path.join(parentDirectory,date)
    if not os.path.exists(date_path):
        os.mkdir(date_path)
    reading_path=os.path.join(date_path,str(reading))
    if not os.path.exists(reading_path):
        os.mkdir(reading_path)
    return reading_path

def ShutDownIf(start_time,dager):
    #turns the RPi off if the time difference between start_time and when the function is called is greater than 'days' number of days
    shutdown_condition=((time.time() - start_time) > (dager*24*60*60) )
    if (shutdown_condition):
        os.system('sudo shutdown')
def ErrorHandler(directory, sensor):
    filename=os.path.join(directory,"error.txt")
    file=open(filename,'a')
    file.write("Error when trying to handle: ")
    file.write(sensor)
    file.write("     /      ")
    file.close()
        

def Mission(runtime=600,samplings_per_day=8,num_sensors=5,days_of_battery=12,start_lag=3600):
    #init
    #runtime=600#in seconds, how long each sensor should read data
    #samplings_per_day=8
    #num_sensors=5
    sleeptime=((24*60*60)/samplings_per_day)-(runtime*num_sensors)
    A=True
    reading_num=1
    print("sleepin")
    time.sleep(start_lag)#gives us 20 minutes from we plug the batteries to when things start
    date=time.strftime("%A- %Y - %m - %d", time.gmtime())
    start_date=time.time()
    while(A):
        ShutDownIf(start_date,days_of_battery) # fist input is when the deployment started, second number is how long we want to run before shutting down (number is in days)
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
        print("I am done with round ",reading_num)
        time.sleep(sleeptime)
        if reading_num==samplings_per_day:
            date=time.strftime("%A- %Y - %m - %d", time.gmtime())
            reading_num=0
            
        reading_num+=1
#print("started")  
#Mission()
#Accelerometer(20, '/home/pi/ping-python/examples/')      
if __name__ == "__main__":
    Mission()
            
        
    
