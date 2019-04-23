import sys # importing open cv library
sys.path.append('/usr/lib/python3/dist-packages/')#we had to add this line as the application was unable to find RPi.GPIO
import RPi.GPIO as GPIO # importing RPi.GPIO
sys.path.append('/usr/local/lib/python3.5/dist-packages/') #we had to add this line as the application was unable to find Bluetooth
import time # importing time library

import cv2 # importing open cv library
import numpy as np # importing numpy library
import bluetooth # importing bluetooth library

bd_addr = "B8:27:EB:5E:BB:A1" #set address of the other pi
port = 1 #set port
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM ) #create a bluetooth socket
sock.connect((bd_addr, port)) #connect to the bluetooth socket

recognizer = cv2.face.LBPHFaceRecognizer_create() #initialising the facial reader
recognizer.read('/home/pi/bigmuscles/FacialRecognitionProject/trainer/trainer.yml') #this file allows the program to recognise pre-taught individuals
cascadePath = "/home/pi/bigmuscles/FacialRecognitionProject/haarcascade_frontalface_default.xml" #this file helps with identifying facial features
faceCascade = cv2.CascadeClassifier(cascadePath); #allowing the program to read faces
font = cv2.FONT_HERSHEY_SIMPLEX #sets font to display names on the live camera feed

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 0.1*cam.get(3) #sets the minimum size a face needs to be for it to be recognised
minH = 0.1*cam.get(4) #sets the minimum size a face needs to be for it to be recognised

#initialise id counter
id = 0

names = ['None', 'Jack', 'Robin' , 'Liam'] #The names of the people that are stored in the datasets

GPIO.setwarnings(False) #set up motion sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN) #set motion sensor as an input


def scanFace():
    while True: #loop forever
        ret, img =cam.read() #read from inputs
        img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #turn image to gray so its easier to read
    
        faces = faceCascade.detectMultiScale(  #make a variable for the face detected
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
       )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #place a rectangle around a face on the live feed if detected (mainly for testing)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w]) #check how certain the program is that its the person its saying

            if (confidence < 60): #if it doesnt match atleast 40% of the person its reading, it wont let the person gain access
                id = names[id] #get the name of the person detected
                confidence = "  {0}%".format(round(100 - confidence)) #display confidence neatly
                sock.send(id) #send signal to other pi saying theres a person detected and tell the other pi who it is.
            else:
                id = "unknown" #default value for somone not on the system.
                confidence = "  {0}%".format(round(100 - confidence))
        
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2) #display "unknown above their face on the live feed for (testing)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) #display the confidence percentage
    
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # if 'ESC' is pressed, the program will stop
        if k == 27:
            break
# Do a bit of cleanup
    print("\n Closing Program")
    cam.release() #turn off camera as input
    cv2.destroyAllWindows() #reset program on close


while True:
    i=GPIO.input(11) #listen for motion sensor
    if i == 0:
        print ("no people near by", i)
        time.sleep(0.1) #keep looping 10 times a second until motion is detected.
    elif i==1:
        print ("face detected!",i) #printing for testing
        scanFace() #run facial recognition method
        time.sleep(5) # wait 5 seconds so that the method isnt called multiple times per one face
        