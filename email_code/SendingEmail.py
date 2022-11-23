import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from random import randint
from time import sleep
import subprocess
import serial
import os
import requests
def ATCommand():
    #['minicom', '-D', '/dev/ttyUSB2', '-b', '115200',  '--script=/home/pi/BashingMyHeadIn',  '--capturefile=/home/pi/minicom-output.txt']
    #"sudo minicom -D /dev/ttyUSB2 -b 115200  --script=BashingMyHeadIn /home/pi/  --capturefile=minicom-output.txt /home/pi/"
    #call=subprocess.Popen(["minicom -D /dev/ttyUSB2 -b 115200  --script=/home/pi/BashingMyHeadIn   --capturefile=/home/pi/minicom-output.txt "],shell=True)
    #output = call.communicate()
    os.system("gnome-terminal 'minicom -D /dev/ttyUSB2 -b 115200  --script=/home/pi/BashingMyHeadIn   --capturefile=/home/pi/minicom-output.txt'")
    
    print("poop")
    
    minicom=open('/home/pi/minicom-output.txt','r')
    for line in minicom:
        print(line)
        
    

def PingPong(filename):
    response_list = subprocess.check_output('ping -s 10 -c 10 google.com',stderr=subprocess.STDOUT,shell=True)
    file=open(filename,'a')
    file.write(str(response_list))
    file.write(" \n \n" )
    response_list=subprocess.check_output('ifconfig',stderr=subprocess.STDOUT,shell=True)
    file.write(str(response_list))
    file.close()
def MakeAFile():
    filename="Attachement.txt"
    with open(filename,"w") as fil:
        fil.write("The time is : ")
        fil.write(str(datetime.now()))
        fil.write("\n \n")
        #rand=randint(0,4)
        #lorem=["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nullam ac tortor vitae purus faucibus. Pharetra vel turpis nunc eget lorem dolor sed. Sed enim ut sem viverra aliquet eget. Iaculis nunc sed augue lacus viverra vitae congue eu. Fermentum dui faucibus in ornare. Interdum posuere lorem ipsum dolor sit. Tincidunt id aliquet risus feugiat in ante metus dictum. Cursus metus aliquam eleifend mi in nulla posuere. Magna fringilla urna porttitor rhoncus dolor purus non enim. Iaculis nunc sed augue lacus viverra vitae congue eu consequat. Sagittis eu volutpat odio facilisis mauris sit. Fringilla phasellus faucibus scelerisque eleifend donec.","Varius morbi enim nunc faucibus a pellentesque sit amet porttitor. Nibh tortor id aliquet lectus proin. Accumsan in nisl nisi scelerisque eu ultrices vitae. Magna etiam tempor orci eu lobortis elementum. Pellentesque eu tincidunt tortor aliquam nulla facilisi cras. Interdum posuere lorem ipsum dolor sit amet consectetur. Risus quis varius quam quisque. Euismod in pellentesque massa placerat duis ultricies. Sed adipiscing diam donec adipiscing. Sed adipiscing diam donec adipiscing tristique risus nec feugiat. Vitae ultricies leo integer malesuada nunc. Fames ac turpis egestas integer eget aliquet nibh praesent tristique. Sed vulputate mi sit amet mauris commodo. Laoreet sit amet cursus sit amet dictum. Tempor id eu nisl nunc mi ipsum faucibus vitae aliquet. Sem viverra aliquet eget sit amet tellus cras adipiscing enim. Quisque non tellus orci ac. Nunc consequat interdum varius sit.","Vulputate odio ut enim blandit. Maecenas accumsan lacus vel facilisis volutpat est velit. Aliquet porttitor lacus luctus accumsan. Sed turpis tincidunt id aliquet risus feugiat. Habitant morbi tristique senectus et netus et malesuada. At urna condimentum mattis pellentesque id. Volutpat consequat mauris nunc congue nisi vitae suscipit. Turpis in eu mi bibendum neque egestas congue quisque. Nisl tincidunt eget nullam non nisi est sit. Bibendum at varius vel pharetra vel turpis nunc. Facilisis volutpat est velit egestas dui id ornare.","Id neque aliquam vestibulum morbi blandit cursus risus at. Vestibulum lectus mauris ultrices eros in cursus turpis massa tincidunt. Metus vulputate eu scelerisque felis. Cursus sit amet dictum sit. At auctor urna nunc id cursus. Pretium fusce id velit ut. Egestas integer eget aliquet nibh praesent tristique magna. Eget dolor morbi non arcu risus. Sit amet mattis vulputate enim nulla aliquet porttitor lacus. Egestas purus viverra accumsan in nisl nisi scelerisque. Sit amet est placerat in egestas erat imperdiet sed euismod. Massa massa ultricies mi quis hendrerit dolor. Pulvinar elementum integer enim neque volutpat ac. Non nisi est sit amet facilisis magna etiam. Imperdiet dui accumsan sit amet. Mollis aliquam ut porttitor leo a diam sollicitudin.","Fermentum posuere urna nec tincidunt praesent semper feugiat nibh sed. Blandit turpis cursus in hac habitasse platea dictumst quisque. Orci porta non pulvinar neque laoreet suspendisse interdum consectetur libero. Dui accumsan sit amet nulla. Sapien pellentesque habitant morbi tristique senectus et. Eget magna fermentum iaculis eu non diam phasellus vestibulum lorem. Proin nibh nisl condimentum id venenatis a condimentum. Erat nam at lectus urna duis. Posuere urna nec tincidunt praesent semper feugiat nibh. Aliquam sem fringilla ut morbi tincidunt augue interdum velit euismod. Elit sed vulputate mi sit amet mauris commodo. Risus quis varius quam quisque id diam vel. Viverra ipsum nunc aliquet bibendum enim facilisis."]
        #fil.write(lorem[rand])
    fil.close()
    PingPong(filename)
    return filename

def SendEmail(filename):
    subject = "4G - connectivity test"
    body = "I am a dwarf and I'm digging a hole, diggy diggy hole /n /n attachment"
    sender_email = "oarpitestmail@gmail.com"
    receiver_email = "simen@oceanaccess.no"
    password ="ExecuteOrder66"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # In same directory as script
    filename="Attachement.txt"


    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}"
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        with open("error-log.txt",'a') as fil:
            fil.write(str(e))
            fil.write("\n \n")
        fil.close()
        
        
def Main():
    for i in range(10):
        try:
            _ = requests.head(url="http://www.google.com/",timeout=5)
        except requests.ConnectionError:
            print("lmao")
            sleep(5)
    sleeptime=300#(24*60*60)/8
    count=0
    while(count<60):
        count+=1
        filename=MakeAFile()
        SendEmail(filename)
        sleep(sleeptime)
Main()


