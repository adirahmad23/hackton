import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response
from pyzbar.pyzbar import decode

app = Flask(__name__)

cap = cv2.VideoCapture("video/adirahmad.mp4")
cap.set(3, 640)
cap.set(4, 480)

with open('dataIdFile.text') as f:
    dataIdWorker = f.read().splitlines()

with open('dataIdVisitor.text') as g:
    dataIdVisitor = g.read().splitlines()


# face recognition
nama = ""
def show_dataset(images_class, label):
    # show data for 1 class
    plt.figure(figsize=(14, 5))
    k = 0
    for i in range(1, 6):
        plt.subplot(1, 5, i)
        try:
            plt.imshow(images_class[k][:, :, ::-1])
        except:
            plt.imshow(images_class[k], cmap='gray')
        plt.title(label)
        plt.axis('off')
        plt.tight_layout()
        k += 1
    plt.show()


dataset_folder = "dataset/"
names = []
images = []
for folder in os.listdir(dataset_folder):
    # limit only 70 face per class
    for name in os.listdir(os.path.join(dataset_folder, folder))[:70]:
        img = cv2.imread(os.path.join(dataset_folder + folder, name))
        images.append(img)
        names.append(folder)
labels = np.unique(names)

for label in labels:

    ids = np.where(label == np.array(names))[0]
    images_class = images[ids[0]: ids[-1] + 1]

face_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_default.xml')


def detect_face(img, idx):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    try:
        x, y, w, h = faces[0]

        img = img[y:y+h, x:x+w]
        img = cv2.resize(img, (100, 100))
    except:
        img = None
    return img


new_names = []
croped_images = []

for i, img in enumerate(images):
    img = detect_face(img, i)
    if img is not None:
        croped_images.append(img)
        new_names.append(names[i])

names = new_names  


for label in labels:
    ids = np.where(label == np.array(names))[0]
    if len(ids) > 0:
        images_class = croped_images[ids[0]: ids[-1] + 1]
    else:
        images_class = []  


name_vec = np.array([np.where(name == labels)[0][0] for name in names])


model = cv2.face.LBPHFaceRecognizer_create()
model.train(croped_images, name_vec)
model.save("lbph_model.yml")
model.read("lbph_model.yml")


def draw_ped(img, label, x0, y0, xt, yt, color=(255, 127, 0), text_color=(255, 255, 255)):

    (w, h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(img,
                  (x0, y0 + baseline),
                  (max(xt, x0 + w), yt),
                  color,
                  2)
    cv2.rectangle(img,
                  (x0, y0 - h),
                  (x0 + w, y0 + baseline),
                  color,
                  -1)
    cv2.putText(img,
                label,
                (x0, y0),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                text_color,
                1,
                cv2.LINE_AA)
    return img


def generate_face_frames():
    global sendLabel, nama
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:

                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))

                idx, confidence = model.predict(face_img)
                label_text = "%s (%.2f %%)" % (labels[idx], confidence)
                nama = labels[idx] 
                print(nama)
                frame = draw_ped(frame, label_text, x, y, x + w, y + h,
                                 color=(0, 255, 255), text_color=(50, 50, 50))
        sendLabel = label_text
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# barcode
def generate_barcode_frames():
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



# website konfigurasi
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
     global sendLabel, nama  # Menggunakan variabel sendLabel dan nama yang didefinisikan di tingkat global
     return render_template('face.php')


if __name__ == "__main__":
    app.run(debug=True)
