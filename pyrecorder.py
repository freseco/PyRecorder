import RPi.GPIO as GPIO
from picamera import PiCamera
import uuid                        #random text
import time
import os
from subprocess import call
import termios
import sys
import tty
import threading

#Script path
path=os.path.dirname(os.path.realpath(__file__))+"/"


# The screen clear function
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')
   # print out some text


camera = PiCamera()

## Display menu     
def print_menu():       
    print (30 * "-" , "Camera Settings" , 30 * "-")
    print ("1. High   quality (1920 ×  1080p @ 30fps)")
    print ("2. Medium quality (1280 × 720p  @ 60fps)")
    print ("3. Low    quality (640 x 480p  @ 60/90fps)")
    print ("5. Exit")
    print (67 * "-")
  
loop=True      
  
while loop:          
    print_menu()    ## Displays menu
    choice = input("Enter your choice [1-5]: ")     
    if choice=='1':     
        print("High quality has been selected")
        camera.resolution = (1920,1080)
        camera.framerate = 15
        loop=False
    elif choice=='2':
        print ("Medium quality has been selected")
        camera.resolution = (1280,720)
        camera.framerate = 20
        loop=False
    elif choice=='3':
        print ("Low quality has been selected")
        camera.resolution = (640,480)
        camera.framerate = 30
        loop=False
    elif choice=='5':
        print ("Menu 5 has been selected")
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        print("Wrong option selection. Enter any key to try again..")


recording=False
namevideofile=""
numvideos=3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

def record():
    global recording
    global namevideofile    
    if recording==False:      
         #camera.start_preview()
        recording=True
        namevideofile=path+str(uuid.uuid4())
        camera.start_recording(namevideofile+'video.h264')
        
        
    print("Recording!")

converting=False 

def ConvertVideo():
    global converting
    converting=True
    #save file as mp4
    print("We are going to convert the video.")
    command = "MP4Box -add "+namevideofile+"video.h264 "+namevideofile+"convertedVideo.mp4"
    # Execute our command
    call([command], shell=True)
    # Video converted.
    print("Video converted.")
    os.remove(namevideofile+"video.h264")
    converting=False

def parargrabar():
    global recording 
    global numvideos   
    if recording==True:
        camera.stop_recording()
        recording=False
        #camera.stop_preview()
        th = threading.Thread(target=ConvertVideo)
        th.start()
        numvideos-=1

def foto():
    camera.start_preview()
    camera.capture(str(uuid.uuid4())+'image.jpg')



while numvideos>0:
  if GPIO.input(3):
    screen_clear()
    print("Press button to record. After "+str(numvideos)+" script will exit.")
    parargrabar()
  else:
    screen_clear()
    record()    
    time.sleep(1)


while converting:
    time.sleep(.5)
    print("Waiting for conversion!")

print("Camera closed.")
camera.close() 