import RPi.GPIO as GPIO
from picamera import PiCamera
import uuid                        #para generar # aleatorios
import time
import os


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
camera.resolution = (800,600)
camera.framerate = 25
grabando=False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

def grabar():
    global grabando
    if grabando==False:#paramos la grabación        
         #camera.start_preview()
        grabando=True
        camera.start_recording(str(uuid.uuid4())+'video.h264')
        
    print("Grabando")
       

def parargrabar():
    global grabando
    if grabando==True:
        camera.stop_recording()
        grabando=False
        #camera.stop_preview()



def foto():
    camera.start_preview()
    camera.capture(str(uuid.uuid4())+'image.jpg')


while True:
  if GPIO.input(3):
    screen_clear()
    print(".....")
    #time.sleep(1)
    parargrabar()
  else:
    screen_clear()
    grabar()    
    time.sleep(1)