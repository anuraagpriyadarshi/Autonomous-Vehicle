from gpiozero import DistanceSensor, Motor
from time import sleep
import cv2
import numpy as np
import urllib.request
import tensorflow as tf

#url='http://192.168.137.28/cam-lo.jpg'
url='http://192.168.137.28/cam-mid.jpg'
#url='http://192.168.137.28/cam-hi.jpg'

# Set up the ultrasonic sensor
sensor = DistanceSensor(echo=24, trigger=23, max_distance=2)

# Set up the motors
left_motor = Motor(forward=7, backward=5)
right_motor = Motor(forward=8, backward=6)

# Load the trained model
model = tf.keras.models.load_model('C:\\----\\----\\----\\trained_m5.h5')

# Define a list of class labels
classLabels = ['Human', 'Vehicle', 'Stop', 'Turn right ahead','Turn left ahead']

# Function to move robot forward
def move_forward(f):
    left_motor.forward(1)
    right_motor.forward(1)
    sleep(1)
    left_motor.forward(f)
    right_motor.forward(f)

# Function to move robot backward
def move_backward(b):
    left_motor.backward(b)
    right_motor.backward(b)

# Function to turn robot left
def turn_left(l):
    left_motor.backward(l)
    right_motor.forward(l)

# Function to turn robot right
def turn_right(r):
    left_motor.forward(r)
    right_motor.backward(r)

# Function to stop robot
def stop():
    left_motor.stop()
    right_motor.stop()

# Function to check for obstacles
def check_obstacle():
    #distance = distance_sensor.distance * 100
    distance = round(sensor.distance * 100, 1)
    print("Distance: ", distance, "cm")
    sleep(0.5)
    return distance 

def object_class():
    # Load and preprocess the image
    cam = cv2.VideoCapture(url)
    while True:
        while True:
            img_resp=urllib.request.urlopen(url)
            imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
            im = cv2.imdecode(imgnp,-1)
    
            cv2.imshow('LIVE',im)
            key=cv2.waitKey(5)
            if key==ord('q'):
                break
        cv2.imwrite('C:\\----\\----\\----\\image.jpg', im) 
        cam.release()
        break    
    cv2.destroyAllWindows()

    image = cv2.imread('C:\\----\\----\\----\\image.jpg')

    image = cv2.resize(image, (64, 64))
    image = image.astype("float64") / 255.0
    image = np.expand_dims(image, axis=0)

    # Make a prediction and get the predicted class label
    classNo = np.argmax(model.predict(image))

    return classNo#,class_name

class_name=classLabels[object_class]

#Operational Behaviour of the vehicle
def obs_behv(class_name):
    if class_name == 'Human':
        print("Human Detected.")
        sleep(10)
        while (check_obstacle()>20):
            move_forward(0.6)
            sleep(1)
            break
        return 
        
    elif class_name == 'Vehicle':
        print("Vehicle Detected.")
        sleep(5)
        while (check_obstacle()>20):
            move_forward(0.6)
            sleep(1)
            break 

    elif class_name == 'Stop':
        print("Stop sign Detected.")
        stop
        return
    
    elif class_name == 'Turn right ahead':
        print("Turn right ahead sign Detected.")
        turn_right(0.6)
        sleep(1)
        move_forward(0.6)
        sleep(1)
        return
    
    elif class_name == 'Turn left ahead':
        print("Turn left ahead sign Detected.")
        turn_left(0.6)
        sleep(1)
        move_forward(0.6)
        sleep(1)
        return
    else :
        print("Unknown obstacle")

# Main loop
while True:
    # Adjust the robot's direction based on the distance reading
    if check_obstacle()>20:
        #move_forward(1)
        #sleep(1)
        move_forward(0.6)
        sleep(1.5)
        #break
    #elif distance > 10:
        #break
    else:
        stop()
        #path_white()
        obs_behv(class_name)
        break
    # Wait a short time before taking the next reading
    sleep(0.1)
    stop()
    run_again = input("Do you want to run the program again? (y/n) ")
    if run_again.lower() != 'y':
        break  