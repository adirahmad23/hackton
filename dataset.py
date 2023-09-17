import os
import cv2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Fungsi untuk menangkap gambar
def capture_images(name):
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    os.makedirs("my_face", exist_ok=True)
    
    i = 0
    while i < 70:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            cv2.resize(frame, (300, 500))
            cv2.imwrite(f"my_face/{name}_{i:04d}.jpg", frame)
            i += 1
    cap.release()

@app.route("/")
def index():
    return render_template("addface.php")

@app.route("/capture", methods=["POST"])
def capture():
    name = request.form.get("name", "DefaultName")

    # Tangkap gambar sebanyak 70 kali
    capture_images(name)

    # Buat direktori dataset jika belum ada
    os.makedirs("dataset/" + name, exist_ok=True)

    # Pindahkan file gambar ke direktori dataset
    os.system(f"move my_face\\* dataset\\{name}\\")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
