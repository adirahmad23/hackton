import cv2

# Buka kamera (sumber video)
cap = cv2.VideoCapture(1)  # Angka 0 biasanya mengacu pada kamera bawaan (webcam) di komputer

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Tidak dapat membuka kamera.")
else:
    print("Kamera berhasil dibuka.")

# Selanjutnya, Anda dapat melakukan berbagai operasi seperti membaca frame dari kamera, mengolah frame, dan menutup kamera saat selesai.

# Baca frame dari kamera
while True:
    ret, frame = cap.read()  # Membaca frame

    if not ret:
        print("Gagal membaca frame.")
        break

    # Tampilkan frame
    cv2.imshow('Webcam', frame)

    # Keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela tampilan
cap.release()
cv2.destroyAllWindows()
