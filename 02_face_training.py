import cv2 # importing the open cv library
import numpy as np # importing the numpy library
from PIL import Image # importing the image library
import os # importing the os library

path = '/home/pi/bigmuscles/FacialRecognitionProject/dataset' # Path for face images database

recognizer = cv2.face.LBPHFaceRecognizer_create() #initialise recogniser
detector = cv2.CascadeClassifier("/home/pi/bigmuscles/FacialRecognitionProject/haarcascade_frontalface_default.xml"); #file to help read facial features

# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #go through each image in the dataset    
    faceSamples=[] #initialise arrays
    ids = [] #initialise arrays

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8') 

        id = int(os.path.split(imagePath)[-1].split(".")[1]) #get ID number for each person
        faces = detector.detectMultiScale(img_numpy) #detect faces

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w]) #for every face detected, add it to the faceSamples variable
            ids.append(id) #add to the ids variable so the IDs match the faceSamples

    return faceSamples,ids

print ("\n Program is learning faces, please wait")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('/home/pi/bigmuscles/FacialRecognitionProject/trainer/trainer.yml') # writes data into the trainier

# Print the numer of faces trained and end program
print("\n {0} faces trained.".format(len(np.unique(ids))))