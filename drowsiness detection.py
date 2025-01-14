import cv2
import os
import numpy as np
from keras.models import load_model
from pygame import mixer

mixer.init()
sound = mixer.Sound("D:/SUBHASHRI/internship/subhashri in sprout/subhashri in sprout/project/driver drowsiness detection system/alarm.mp3")

face = cv2.CascadeClassifier("D:/SUBHASHRI/internship/subhashri in sprout/subhashri in sprout/project/driver drowsiness detection system/haarcascade_frontalface_alt.xml")
leye = cv2.CascadeClassifier("D:/SUBHASHRI/internship/subhashri in sprout/subhashri in sprout/project/driver drowsiness detection system/haarcascade_lefteye_2splits.xml")
reye = cv2.CascadeClassifier("D:/SUBHASHRI/internship/subhashri in sprout/subhashri in sprout/project/driver drowsiness detection system/haarcascade_righteye_2splits.xml")

lbl = ['Close', 'Open']

model = load_model("D:/SUBHASHRI/internship/subhashri in sprout/subhashri in sprout/project/driver drowsiness detection system/cnnCat2.h5")
path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
count = 0
score = 0
thicc = 2

while (True):
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
    left_eye = leye.detectMultiScale(gray)
    right_eye = reye.detectMultiScale(gray)

    cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

    rpred = None
    lpred = None

    for (x, y, w, h) in right_eye:
        r_eye = frame[y:y + h, x:x + w]
        count = count + 1
        r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye, (24, 24))
        r_eye = r_eye / 255
        r_eye = r_eye.reshape(24, 24, -1)
        r_eye = np.expand_dims(r_eye, axis=0)
        rpred = model.predict(r_eye)
        if np.argmax(rpred) == 1:
            lbl = 'Open'
        else:
            lbl = 'Closed'
        break

    for (x, y, w, h) in left_eye:
        l_eye = frame[y:y + h, x:x + w]
        count = count + 1
        l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
        l_eye = cv2.resize(l_eye, (24, 24))
        l_eye = l_eye / 255
        l_eye = l_eye.reshape(24, 24, -1)
        l_eye = np.expand_dims(l_eye, axis=0)
        lpred = model.predict(l_eye)
        if np.argmax(lpred) == 1:
            lbl = 'Open'
        else:
            lbl = 'Closed'
        break

    if rpred is not None and lpred is not None:
        if np.argmax(rpred) == 0 and np.argmax(lpred) == 0:
            score = score + 1
            cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            score = score - 1
            cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    if score < 0:
        score = 0
    cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    if score > 15:
        cv2.imwrite(os.path.join(path, 'image.jpg'), frame)
        try:
            sound.play()
        except:
            pass
        if thicc < 16:
            thicc = thicc + 2
        else:
            thicc = thicc - 2
            if thicc < 2:
                thicc = 2
        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
