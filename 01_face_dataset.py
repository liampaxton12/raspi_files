import cv2 # importing the open cv library 
import os  # importing the os library
cam = cv2.VideoCapture(0) #set up camera
cam.set(3, 640) # setting video width
cam.set(4, 480) # setting video height
face_detector = cv2.CascadeClassifier('/home/pi/bigmuscles/Cascades/haarcascade_frontalface_default.xml') #absolute address of file to let the program recognise faces
# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ') #asks the user for an int value to associate with the face its viewing
print("\n Look the camera and wait") #tells the user to wait for the photos to be taken

count = 0 #initialise count variable

while(True):
    ret, img = cam.read() #read from camera
    img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #define gray
    faces = face_detector.detectMultiScale(gray, 1.3, 5) #set the image to gray so its easier to read
    for (x,y,w,h) in faces: #for every face that it can detect, do this
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) #place a rectangle over their face in the camera's live feed for testing
        count += 1 #add one to the count 
        cv2.imwrite("/home/pi/bigmuscles/FacialRecognitionProject/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w]) # Save the captured image into the datasets folder with a unique file name
        cv2.imshow('image', img) #display image on screen for testing
    k = cv2.waitKey(100) & 0xff # 'ESC' will close the program
    if k == 27:
        break
    elif count >= 30: # Take 30 face samples and stop taking photos
         break
# Do a bit of cleanup
print("\n Thank you, processing images.")
cam.release() #stop using camera
cv2.destroyAllWindows() #close windows