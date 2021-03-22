from scipy.spatial import distance as dist 
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np 
import playsound
import argparse
import imutils
import time
import dlib 
import cv2 
import RPi.GPIO as GPIO

#play sound
def sound_alarm(path):
    playsound.playsound(path)

#compute the ratio of distances between the vertial eye landmarks and the distances between the horizonal eye landmarks
def eye_aspect_ratio(eye):
    #vertical eye landmarks (x,y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    #compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

#parse the commandline
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True, help= "path to where the face cascade resides") #--cascade is the path to the Haar cascade XML file used for face detection
ap.add_argument("-p", "--shape-predictor", required=True, help= "path to facial landmark predictor") #--shape-predictor is the path to the dlib facial landmark predictor file
ap.add_argument("-a", "--alarm", type=int, default=0, help= "boolean used to indicate if TrafficHat should be used") #--alarm is a boolean to indicate if the TrafficHat buzzer should be used when drowsiness is detected
ap.add_argument("-w", "--webcam", type=int, default=0, help= "index of webcam on system")
args = vars(ap.parse_args())

#check to see if we are using GPIO/TrafficHat as an alarm
if args["alarm"] > 0:
    from gpiozero import TrafficHat
    th = TrafficHat()
    print("[INFO] using TrafficHat alarm ...")

#define variables
EYE_AR_THRESH = 0.3 #If the eye aspect ratio falls below this threshold, we’ll start counting the number of frames the person has closed their eyes for.
EYE_AR_CONSEC_FRAMES = 48 #If the number of frames the person has closed their eyes in exceeds, we'll sound an alarm

COUNTER = 0 #the total number of consecutive frames where the eye aspect ratio is below EYE_AR_THRESH
ALARM_ON = False

#initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
print("[INFO] loading facial landmark predictor ....")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

#extract the eye regions from a set of facial landmarks
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#core of drowsiness detector
print("[INFO] starting video stream thread ...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

#loop over frames from the video stream
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect faces in the grayscale frame
    rects = detector(gray, 0)

    #loop over the face detections
    for rect in rects:
        #determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        #extract left and right eye coordinates, then use the coordinate to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        #average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        #compute the convex hull for the left and right eye, then visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frames, [leftEyeHull], -1, (0,255,0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0,255,0), 1)

        #check to see if the eye aspect ratio is below the blink threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            COUNTER += 1 

            #if the eye were closed for a sufficient number of then sound the alarm
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True

                    if args["alarm"] != "":
                        t = Thread(target=sound_alarm, args=(args["alarm"],))
                        t.daemon = True
                        t.start()

                #draw an alarm on the frame
                cv2.putText(frame, "Drowsiness Alert!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            COUNTER = 0
            ALARM_ON = False
            cv2.putText(frame, "EAR: {:2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    #show the frame 
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    #if the 'q' key was pressed, break from the loop
    if key == ord('q'):
        break

cv2.destroyAllWindows()
vs.stop()

''' Running command line to execute this file: 
$ python detect_drowsiness.py \
	--shape-predictor shape_predictor_68_face_landmarks.dat \
	--alarm alarm.wav '''