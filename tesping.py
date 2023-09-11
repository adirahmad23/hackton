from flask import Flask, render_template, Response, request
import os
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Inisialisasi objek pemindaian kode batang
barcode_cap = cv2.VideoCapture(0)
barcode_cap.set(3, 640)
barcode_cap.set(4, 480)

with open('dataIdFile.text') as f:
    dataIdWorker = f.read().splitlines()

with open('dataIdVisitor.text') as g:
    dataIdVisitor = g.read().splitlines()

# Inisialisasi objek pengenalan wajah
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
model = cv2.face_LBPHFaceRecognizer.create()
dataset_folder = "dataset/"
labels = []
images = []

for folder in os.listdir(dataset_folder):
    for name in os.listdir(os.path.join(dataset_folder, folder))[:70]:
        img = cv2.imread(os.path.join(dataset_folder + folder, name), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            labels.append(folder)

unique_labels = np.unique(labels)
name_to_label = {name: label for label, name in enumerate(unique_labels)}
labels = [name_to_label[name] for name in labels]

model.train(images, np.array(labels))
model.save("lbph_model.yml")
model.read("lbph_model.yml")

def generate_face_frames():
    while True:
        success, img = barcode_cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            face_img = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
            idx, confidence = model.predict(face_img)
            label_text = f"{unique_labels[idx]} ({confidence:.2f} %)"
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_barcode_frames():
    while True:
        success, img = barcode_cap.read()
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

@app.route('/')
def index():
    return render_template('index.php')

@app.route('/video_feed_face')
def video_feed_face():
    return Response(generate_face_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_barcode')
def video_feed_barcode():
    return Response(generate_barcode_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan')
def scan():
    return render_template('barcode.php')

@app.route('/face')
def face():
    return render_template('face.php')

if __name__ == "__main__":
    app.run(debug=True)
