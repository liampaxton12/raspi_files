import bluetooth
import time
from multiprocessing import process
import sys
from sense_hat import SenseHat
sense = SenseHat()

r = (255,0,0)
w = (255,255,255)
redLock =[
    w,r,r,r,r,r,r,w,
    r,w,r,r,r,r,w,r,
    r,r,w,r,r,w,r,r,
    r,r,r,w,w,r,r,r,
    r,r,r,w,w,r,r,r,
    r,r,w,r,r,w,r,r,
    r,w,r,r,r,r,w,r,
    w,r,r,r,r,r,r,w
    ]

sense.set_pixels(redLock)

data = ""
server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 1
server_sock.bind(("",port))
server_sock.listen(1)
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)


def unlocked():
    sense.show_message("UNLOCKED")

g = (0,255,0)



greenUnlock =[
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,w,g,
    g,g,g,g,g,w,g,g,
    g,g,w,g,w,g,g,g,
    g,g,g,w,g,g,g,g,
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,g,g
    ]



while True:
    #if input() ==True: #if button is pressed
        #sense.set_pixels(greenUnlock) #unlock door
        #time.sleep(5) #wait 5 seconds
        #sense.set_pixels(redLock) #lock the door again
    data=""
    data = client_sock.recv(1024)
    #sense.show_message((str)(data[1:]))
    sense.set_pixels(greenUnlock)
    time.sleep(5)
    sense.set_pixels(redLock)
    client_sock.close()
    server_sock.close()