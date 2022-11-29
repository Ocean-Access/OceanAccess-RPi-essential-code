from __future__ import print_function
import time
import smbus
from dual_g2_hpmd_rpi import motors, MAX_SPEED
from pyudev import Context, Devices
import serial
from brping import Ping1D
import math
import time
import datetime
import sys
import os
import requests
sys.path.append("/home/pi/ping-python/kellerLD")
try:
    from kellerLD import KellerLD
except:
    pass
import argparse
import calendar
from builtins import input

BAUDRATE = 9600

class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)
        
def FindCorrectPort(examplecommand):
    for i in range(5):
        print(f"Trying ttyUSB{i}")
        try:
            ser = serial.Serial(f"/dev/ttyUSB{i}", baudrate=BAUDRATE)
            ser.write(examplecommand)
            time.sleep(1)
            reading = ser.read(ser.inWaiting())
            if len(reading) > 0:
                print(f"Identified correct port {i}")
                print(reading)
                return f"/dev/ttyUSB{i}"
        except Exception as e:
            print(f"ttyUSB{i} was not the right port. The Exception is {e}")
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
    try:
        myPing = Ping1D()
        myPing.connect_serial("/dev/ttyUSB_BRS", 115200)
    except:
        for i in range(5):
            try:
                myPing = Ping1D()
                myPing.connect_serial(f"/dev/ttyUSB{i}", 115200)
                break
            except:
                pass
    start = time.time()
    data_list = []
    while (time.time() - start < runtime):
        data = myPing.get_distance()
        if data:
            data_list.append("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
        else:
            data_list.append("Distance: NONE \tConfidence: NONE")
    filename=os.path.join(directory,"BlueRoboticsSonar.txt")
    file=open(filename,'a')
    file.write("\nsampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n", time.gmtime()))
    file.write("\n".join(data_list))
    file.close()

def BlueRoboticsPressureSensor(runtime,directory):
    sensor = KellerLD()
    sensor.init()
    filename=os.path.join(directory,"BlueRoboticsPressure.txt")
    file=open(filename,'a')
    file.write("sampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n", time.gmtime()))
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
    bus.write_i2c_block_data(0x18,0x10,[0x02]) #skal vaerer 0x02 på slutten
    firstcommand=("#p\r").encode()
    secondcommand=("#o\r").encode()
    time.sleep(5)
    port=FindCorrectPort(firstcommand)
    if port==None:
        bus.write_i2c_block_data(0x18,0x10,[0x00])
        raise Exception("Port not found error")
    ser = serial.Serial(port, baudrate=BAUDRATE)    #Open named port 
    raiseIfFault() #check if the motor hat has gone to shit
    #motors.motor1.setSpeed(MAX_SPEED)
    time.sleep(5)
    
    timer=0
    start=time.time()
    data = []
    data2 = []
    # Need to find a better way to wait until data is processed before reading
    # These times seem to work, but it would be better to poll the sensor to see if it is done or something.
    while (time.time()-start< runtime):
        ser.write(firstcommand)                         #send command string                
        reading=ser.readline()               #read data in read buffer
        data.append(reading.decode())
        ser.write(secondcommand)
        reading2=ser.readline()
        data2.append(reading2.decode())
    # write to files
    filename=os.path.join(directory,"ISA500.txt")
    file=open(filename,'a') #next three lines are to open a file and start writing to it
    file.write("\nsampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n", time.gmtime()))
    filename2=os.path.join(directory,"ISA500-ahrs.txt")
    file2=open(filename2,'a') #next three lines are to open a file and start writing to it
    file2.write("\nsampling started at :")
    file2.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n", time.gmtime()))
    file.write("".join(data))
    file2.write("".join(data2))
    ser.close()
    file.close()
    file2.close()
    bus.write_i2c_block_data(0x18,0x10,[0x00])
    
def ISD4000(runtime, directory,port="/dev/ttyUSB_IDD"):
    bus=smbus.SMBus(1)
    bus.write_i2c_block_data(0x18,0x10,[0x01]) #sskal vaere 0x02 paa sluttne
    firstcommand=("#d\r").encode()
    secondcommand=("#o\r").encode()
    time.sleep(5)
    port=FindCorrectPort(firstcommand)
    if port==None:
        bus.write_i2c_block_data(0x18,0x10,[0x00])
        raise Exception("Port not found error")
    ser = serial.Serial(port, baudrate=BAUDRATE)    #Open named port 

    raiseIfFault() #check if the motor hat has gone to shit
    #motors.motor2.setSpeed(MAX_SPEED)
    #time.sleep(5)
    
    data = []
    data2 = []
    start = time.time()
    starts = []
    ends = []
    while (time.time() - start < runtime):
        starts.append(time.time())
        ser.write(firstcommand)                         #send command string        
        reading=ser.readline()              #read data in read buffer
        data.append(reading.decode())
        ser.write(secondcommand)
        reading2=ser.readline()
        data2.append(reading2.decode())
        ends.append(time.time())
    filename=os.path.join(directory,"ISD4000.txt")
    file=open(filename,'a') #next three lines are to open a file and start writing to it
    file.write("\nsampling started at :")
    file.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n", time.gmtime()))
    filename2=os.path.join(directory,"ISD4000-ahrs.txt")
    file2=open(filename2,'a') #next three lines are to open a file and start writing to it
    file2.write("\nsampling started at :")
    file2.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000 \n ", time.gmtime()))
    file.write("".join(data))
    file2.write("".join(data2))
    ser.close()
    file.close()
    file2.close()

    # Send to web
    req_string = f"water-test,{datetime.datetime.now().isoformat()},{len(data) / runtime}\n"
    req_string += "".join(data)
    r = requests.put("http://192.168.1.13:3000/data", headers={'content-type': 'text/isd4000'}, data=req_string)
    print(r)

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
def ErrorHandler(directory, sensor, error):
    filename=os.path.join(directory,"error.txt")
    file=open(filename,'a')
    file.write("Error when trying to handle: ")
    file.write(sensor)
    file.write(str(error))
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
        except Exception as e:
            print(e)
            ErrorHandler(directory,"ISA500",e)
        try:
            ISD4000(runtime,directory)
        except Exception as e:
            print(e)
            ErrorHandler(directory,"ISD4000",e)
        try:
            BlueRoboticsSonar(runtime,directory)
        except Exception as e:
            ErrorHandler(directory,"Blue Robotics Sonar", e)
        try:
            BlueRoboticsPressureSensor(runtime,directory)
        except Exception as e:
            ErrorHandler(directory,"Blue Robotics Pressure Sensor", e)
        try:
            Accelerometer(runtime,directory)
        except Exception as e:
            ErrorHandler(directory,"Accelerometer",e)
                
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
            
        
    
