import os
import cv2
import sys
import time

# Mengambil nama dari argumen yang diberikan di terminal
my_name = sys.argv[1] if len(sys.argv) > 1 else "DefaultName"

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
def show_countdown(count):
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 2
    color = (0, 255, 0)
    thickness = 3
    text = f"Capture in {count}"

    text_size = cv2.getTextSize(text, font, size, thickness)[0]
    text_x = (cap.get(cv2.CAP_PROP_FRAME_WIDTH) - text_size[0]) // 2
    text_y = (cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - text_size[1]) // 2

    ret, frame = cap.read()
    if ret:
        cv2.putText(frame, text, (int(text_x), int(text_y)), font, size, color, thickness)
        cv2.imshow("Capture Photo", frame)

# Menampilkan countdown sebelum mulai menangkap
for countdown in range(10, 0, -1):
    show_countdown(countdown)
    cv2.waitKey(1000)  # Menunggu 1 detik

# Mulai menangkap gambar
i = 0
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Argument 1 berarti flip horizontal
    if ret:
        cv2.resize(frame, (300, 500))
        cv2.imshow("Capture Photo", frame)
        cv2.imwrite("my_face/%s_%04d.jpg" %  (my_name, i), frame)
        
        if cv2.waitKey(100) == ord('q') or i == 70:
            break
        i += 1

cap.release()
cv2.destroyAllWindows()

# Memindahkan file gambar ke direktori dataset
os.makedirs("dataset/" + my_name, exist_ok=True)
os.system("move my_face\\* dataset\\" + my_name + "\\")
