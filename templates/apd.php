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

        #recognize-button {
            margin: 280px;
            margin-top: 30px;
            padding: 20px 80px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            background-color: #3498db;
            color: #fff;
            border: none;
            cursor: pointer;
        }

        .responsive-img {
            width: 750px;
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
            background-color: #3498db;
            color: #fff;
            padding: 10px 10px;
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

        #namaInput {
            font-size: 40px;
            border: none;
            text-align: center;
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
            <img id="video_stream" src="{{ url_for('video_feed_apd') }}" class="responsive-img"> 
        </div>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <button id="recognize-button" class="rounded-button">CETAK PDF</button>
    </div>

    <footer class="footer">
        <div class="footer-content">
            <img src="{{ url_for('static', filename='fotter.png') }}" alt="ISAFE Logo" width="1080px" height="120px">
        </div>
    </footer>
    
    <script>
        var video = document.getElementById('video_stream');

        function updateVideo() {
            video.src = "{{ url_for('video_feed_apd') }}";
            setTimeout(updateVideo, 1000);  // Update video every 1 second
        }

        updateVideo();
    </script>

    <script>
      
    </script>

</body>

</html>
