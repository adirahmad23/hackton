<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Recognition Website</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }

        .header {
            text-align: center;
            padding: 20px;
            background-color: #ffffff;
            color: #fff;
        }

        .content {
            text-align: center;
            margin: 150px;
        }

        #video-container {
            max-width: 100%;
            margin: 100 auto;
            transform: rotate(90deg);
        }

        #video {
            width: auto;
            height: auto;
        }

        .button-input {
            margin-top: 240px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        #barcodeInput {
            font-size: 40px;
            border: none;
            text-align: center;
            margin: 20px 0; /* Jarak atas dan bawah */
        }

        #recognize-button {
            padding: 20px 80px;
            font-size: 30px;
            background-color: #3498db;
            color: #fff;
            border: none;
            cursor: pointer;
            border-radius: 20px;
        }

        .responsive-img {
            width: 1000px;
            height: auto;
        }

        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
            padding: 20px;
        }

        .image-container img {
            max-width: 25%;
            height: auto;

        }

        .rounded-button {
            border-radius: 20px;
            /* Sesuaikan angka ini sesuai dengan sudut yang Anda inginkan */
            background-color: #3498db;
            color: #fff;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            border: none;
        }

        .footer {
            color: #fff;
            text-align: center;
            padding-bottom: -100px;
            padding: -4px;
            position: fixed;
            bottom: 0;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }

    </style>
</head>

<body>
    <div class="image-container">
        <img src="{{ url_for('static', filename='sucofindo.png') }}" alt="Sucofindo Logo">
        <img src="{{ url_for('static', filename='Logo_ISAFE.png') }}" alt="ISAFE Logo">
    </div>

    <div class="content">
        <div id="video-container">
            <img src="{{ url_for('video_feed_barcode') }}" class="responsive-img">
        </div>
        <div class="button-input">
            <input type="text" id="barcodeInput" placeholder="Hasil barcode" style="font-size: 40px;" disabled>
            <button onclick="window.location.href='/face'" id="recognize-button" class="rounded-button">ID</button>
        </div>
    </div>

    <footer class="footer">
        <div class="footer-content">
            <img src="{{ url_for('static', filename='fotter.png') }}" alt="ISAFE Logo" width="1080px" height="120px">
        </div>
    </footer>

    <script>
    const barcodeInputElement = document.getElementById('barcodeInput');

    function updateBarcode() {
        fetch('/get_barcode')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Permintaan gagal: ' + response.statusText);
                }
                return response.text();
            })
            .then(data => {
                if (data) {
                    // Jika ada data dalam input teks, arahkan ke halaman lain
                    window.location.href = '/face'; // Ganti dengan URL halaman tujuan
                }
                barcodeInputElement.value = data;
            })
            .catch(error => {
                console.error('Gagal mendapatkan barcode:', error);
                barcodeInputElement.value = 'Gagal mendapatkan barcode'; // Menampilkan pesan kesalahan di input teks
            });
    }
    setInterval(updateBarcode, 1000);
</script>


</body>

</html>
