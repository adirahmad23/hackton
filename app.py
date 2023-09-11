from flask import Flask, render_template, Response
import os
import cv2
import numpy as np

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
model = cv2.face.LBPHFaceRecognizer_create()
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

cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            face_img = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
            idx, confidence = model.predict(face_img)
            label_text = f"{unique_labels[idx]} ({confidence:.2f} %)"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # label_response = f"{label_text}\n"

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  


@app.route('/')
def index():
    return render_template('index.php')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
