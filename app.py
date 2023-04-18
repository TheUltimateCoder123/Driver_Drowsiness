from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model
from pygame import mixer

app = Flask(__name__)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
model = load_model(r'G:\Projects\Driver_Drowsiness\model\model.h5')

mixer.init()
sound= mixer.Sound(r'G:\Projects\Driver_Drowsiness\detection\alarm.wav')

cap = cv2.VideoCapture(0)
Score = 0
prev_state = None
prev_score = None


def detect_drowsiness():
    global Score, prev_state, prev_score
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
        
        cv2.rectangle(frame, (0, height-50), (200, height), (0, 0, 0), thickness=cv2.FILLED)
        state = None
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, pt1=(x, y), pt2=(x+w, y+h), color=(255, 0, 0), thickness=3)
            
        for (ex, ey, ew, eh) in eyes:
            eye = frame[ey:ey+eh, ex:ex+w]
            eye = cv2.resize(eye, (80, 80))
            eye = eye/255
            eye = eye.reshape(80, 80, 3)
            eye = np.expand_dims(eye, axis=0)
            prediction = model.predict(eye)
            
            if prediction[0][0] > 0.30:
                state = 'closed'
                Score = Score+1 if prev_state != 'closed' else Score
                if Score > 10:
                    try:
                        sound.play()
                    except:
                        pass
            else:
                state = 'open'
                Score = Score-2 if prev_state == 'closed' else Score
                if Score < 0:
                    Score = 0
                    
        prev_state = state
        
        if state is not None:
            cv2.putText(frame, state, (10, height-20), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.75, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        
        if Score != prev_score:
            cv2.putText(frame, 'Score: '+str(Score), (100, height-20), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.75, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
            prev_score = Score
                
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(detect_drowsiness(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
