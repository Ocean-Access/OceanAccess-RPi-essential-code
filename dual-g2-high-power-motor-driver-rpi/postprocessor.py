import pandas as pd 
import os
import re
import sys
import time, datetime
def SintefData():
    #this one takes the data from Sintef and saves it into a .csv

    return


def TimeStamper(frequency, start_time,data):
    #adds timestamp to the data
    #use pandas

    # converting time string into Unix Epoch
    RPi_time=time.mktime(datetime.datetime.strptime(start_time, "%a, %d %b %Y %H:%M:%S +0000").timetuple())


    #must be measured while putting the pi out
    #time_error is the difference between time measured by RPi and the real time, measured in seconds since Jan 1st 1970
    time_error=69 #placeholder number
    timestamps=[]
    timestamps.append(RPi_time+time_error)
    for i in data:
        
        timestamps.append(timestamps[-1]+(1/frequency))
    




    return timestamps




def ISD4000(path):
    #walking through the folder and subfolders to find all the files
    list_of_files=[]
    for folder in os.walk(path):
        for filename in folder[2]:
            if filename.__contains__('ISD4000'):
                list_of_files.append(os.path.join(folder[0],filename))
    #opening each file and reading the data
    for file in list_of_files:
        
        with open(file) as fil:
            depth=[]
            pressure=[]

            heading=[]
            pitch=[]
            roll=[]
            for line in fil:
                # TODO read start of file, which should contain start-time
                if line.__contains__("sampling started at :"):
                    a=line.find("sampling started at :")
                    start_time=line[a:a+32]


                #finding all instances of 
                # $ISDPT,dddd.ddd,M,ppp.pppp,B,tt.tt,C*xx<CR><LF> where
                # ddd.ddd = depth in meters
                # ppp.pppp = absolute pressure in Bar
                # tt.tt= temperature in Celsius
                # xx = NMEA standard checksum
                for match in re.finditer('(\$ISDPT,([0-9]|-){4}.[0-9]{3},M,([0-9]|-){3}.[0-9]{4},B)',line):
                    reading=match.group(0)
                    data=reading.split(',')

                    # TODO find out what to do with code below

                    depth.append(data[1])#reading[7:15]
                    pressure.append(data[2])#reading[18:26]
                

                #finding all instances of
                # $ISHPR,hhh.h,spp.p,srrr.r*xx<CR><LF> where
                # s = sign + or -
                # hhh.h = heading in degrees (0 to 359.9)
                # pp.p = pitch in degrees (90.0 to -90.0)
                # rrr.r = roll in degrees (180.0 to -180.0)
                # xx = NMEA standard checksum
                for match in re.finditer('(\$ISHPR,([0-9]|-|+){3}.[0-9],([0-9]|-|+){2}.[0-9],([0-9]|-|+){3}.[0-9])',line):
                    reading=match.group(0)
                    data=reading.split(',')

                    #TODO find out what to do with code below

                    heading.append(data[1])#reading[7:12]
                    pitch.append(data[2])#reading[13:18]
                    roll.append(data[3])#reading[19:25]  
            ISD_pressure_time=TimeStamper(10,start_time,depth)
            ISD_heading_time=TimeStamper(10,start_time,heading)


def ISA500(path):
    #walking through the folder and subfolders to find all the files
    list_of_files=[]
    
    for folder in os.walk(path):
        for filename in folder[2]:
            if filename.__contains__('ISA500'):
                list_of_files.append(os.path.join(folder[0],filename))
    #opening each file and reading the data
    for file in list_of_files:
        
        with open(file) as fil:
            
            distance=[]
            energy_level=[]
            correlation_factor=[]

            accel_x=[]
            accel_y=[]
            accel_z=[]

            gyro_x=[]
            gyro_y=[]
            gyro_z=[]

            magneto_x=[]
            magneto_y=[]
            magneto_z=[]
            for line in fil:
                # TODO read start of file, which should contain start-time
                if line.__contains__("sampling started at :"):
                    a=line.find("sampling started at :")
                    start_time=line[a:a+32]


                #finding all instances of 
                # $ISADI,ddd.ddd,M,e.eeee,c.cccc,tt.t,C*xx<CR><LF> where
                # ddd.ddd = distance in meters from the transducer face to the target.
                # e.eeee = energy level (0 to 1)
                # c.cccc = correlation factor (0 to 1)
                # tt.t = temperature in Celsius
                # xx = NMEA standard checksum
                for match in re.finditer('(\$IADI,([0-9]|-){3}.[0-9]{3},M,([0-9]|-).[0-9]{4},([0-9]).([0-9]){4})',line):    
                    reading=match.group(0)
                    data=reading.split(',')

                   

                    distance.append(data[1])
                    energy_level.append(data[2])
                    correlation_factor.append(data[3])

                

                #finding all instances of
                # $ISAGM,a.aaa,a.aaa,a.aaa,g.ggg,g.ggg,g.ggg,m.mmm,m.mmm,m.mmm*xx<CR><LF> where
                # a.aaa = Accelerometer reading: X then Y then Z
                # g.ggg = Gyroscope reading: X then Y then Z
                # m.mmm = magnetometer reading: X then Y then Z
                # xx = NMEA standard checksum
                #'(\$ISAGM,([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3})'
                for match in re.finditer('(\$ISAGM,([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3},([0-9]|-){1,2}.([0-9]){3})',line): 
                    reading=match.group(0)
                    data=reading.split(',')
                    
                    accel_x.append(data[1])
                    accel_y.append(data[2])
                    accel_z.append(data[3])

                    gyro_x.append(data[4])
                    gyro_y.append(data[5])
                    gyro_z.append(data[6])

                    magneto_x.append(data[7])
                    magneto_y.append(data[8])
                    magneto_z.appen(data[9])
        ISA_echo_timer=TimeStamper(4,start_time,distance)
        ISA_heading_timer=TimeStamper(4,start_time,accel_x) #TODO check Hz
    # TODO create dataframe, add timestamps



                   
                    
                    
def Bar100(path):
    list_of_files=[]
    for folder in os.walk(path):
        for filename in folder[2]:
            if filename.__contains__('BlueRoboticsPressure'):
                list_of_files.append(os.path.join(folder[0],filename))
    

    for file in list_of_files:
        with open(file) as fil:
            for line in fil:
                if line.__contains__("sampling started at :"):
                    a=line.find("sampling started at :")
                    start_time=line[a:a+32]
                    
                else:
                    readings=line.split(',')
                    print(readings)
                    # TODO create dataframe, add timestamps
        Bar100_timestamp=TimeStamper(10,start_time,readings)

def BlueRoboticsSonar(path):
    list_of_files=[]
    for folder in os.walk(path):
        for filename in folder[2]:
            if filename.__contains__('BlueRoboticsPressure'):
                list_of_files.append(os.path.join(folder[0],filename))
    for file in list_of_files:
        with open(file) as fil:
            distance=[]
            confidence=[]
            for line in fil:
                if line.__contains__("sampling started at :"):
                    a=line.find("sampling started at :")
                    start_time=line[a:a+32]
                else:
                    #Distance: NONE 	Confidence: NONED
                      for match in re.finditer('Distance: ([0-9]+|NONE) [\t]Confidence: ([0-9]+|NONE)',line):
                        reading=match.group(0)
                        distance.append(reading[9:14])
                        confidence.append(reading[-5:-1])
                        # TODO create dataframe, add timestamps
        BRS_timestamp=TimeStamper(4,start_time,distance) # TODO check Hz

def Accelerometer(path):
    list_of_files=[]
    for folder in os.walk(path):
        for filename in folder[2]:
            if filename.__contains__('Accelerometer'):
                list_of_files.append(os.path.join(folder[0],filename))
    for file in list_of_files:
        with open(file) as fil:
            for line in fil:
                if line.__contains__("sampling started at :"):
                    a=line.find("sampling started at :")
                    start_time=line[a:a+32]
                else:
                    #Distance: NONE 	Confidence: NONED
                      for match in re.finditer('Distance: ([0-9]+|NONE) [\t]Confidence: ([0-9]+|NONE)',line):
                        reading=match.group(0)
                        distance=reading[9:14]
                        confidence=reading[27:-1]
                        # TODO find out what to do with this list of readings
        TimeStamper(6.25,start_time,distance)
    

def ReadAllData():
    #does three things
    #1 . tells each postprocessor what day to look at, and where to store those files
    # 2. combines all files from postprocessors into master doc
    # 3. 

    #finding folder of day
    path="lol"

    for placement in range(10):
        ISA500(path)
        ISD4000(path)
        Bar100(path)
        BlueRoboticsSonar(path)
        Accelerometer(path)
    





def ScrewingAround():

    data=[1,2,3,4,5,6,7,8,9,10]
    start_time="Tue, 26 Oct 2021 03:12:48 +0000"

    frequency=10 #Hz

    taaiim=TimeStamper(frequency,start_time,data)
    print(taaiim)

    #file=r"C:\Users\simen\Desktop\OA\Dory\BlueRoboticsSonar.txt"
    #with open(file) as fil:
    #        for line in fil:
    #            if line.__contains__("sampling started at :"):
    #                #TODO figure out how we implement this
    #                print(line)
    #            else:
    #                #Distance: NONE 	Confidence: NONED
    #                for match in re.finditer('Distance: ([0-9]+|NONE) [\t]Confidence: ([0-9]+|NONE)',line):
    #                    reading=match.group(0)
    #                    distance=reading[9:14]
    #                    confidence=reading[27:-1]
    #                    # TODO find out what to do with this list of readings

ScrewingAround()  
#Bar100(r'C:\Users\simen\Desktop\OA\Dory\Monday- 2021 - 10 - 25')
#for m in re.finditer(pattern, s):
#    print m.group(2), '*', m.group(1)
