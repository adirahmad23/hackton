import cv2
import numpy as np
from pyzbar.pyzbar import decode
from flask import Flask, render_template, Response

app = Flask(__name__)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open('dataIdFile.text') as f:
    dataIdWorker = f.read().splitlines()

with open('dataIdVisitor.text') as g:
    dataIdVisitor = g.read().splitlines()

def generate_frames():
    while True:
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')

            if myData in dataIdWorker:
                myOutput = 'ID Pekerja = ' + myData
                myColor = (0, 255, 0)
            elif myData in dataIdVisitor:
                myOutput = 'ID Visitor = ' + myData
                myColor = (255, 0, 0)
            else:
                myOutput = 'ID tidak terdaftar = ' + myData
                myColor = (0, 0, 255)

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, myColor, 2)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/barcode')
def index():
    return render_template('barcode.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
