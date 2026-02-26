from flask import Flask, Response, jsonify, render_template_string
from lib.video_stream import generate_frames
from lib.data_generator import get_engineering_data
from lib.config import Config

app = Flask(__name__)

HTML_PAGE = """
<html>
<head>
<title>Video Stream Monitor</title>
<script>
function updateData(){
    fetch('/data')
    .then(res => res.json())
    .then(data => {
        document.getElementById("data").innerHTML =
        "Time: " + data.time + " s<br>" +
        "Temp: " + data.temperature + " °C<br>" +
        "Voltage: " + data.voltage + " V<br>" +
        "Speed: " + data.speed + " m/s";
    });
}
setInterval(updateData, 1000);
</script>
</head>
<body>
<h2>Video Stream</h2>
<img src="/video_feed" width="640">
<h2>Engineering Data</h2>
<div id="data"></div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    return jsonify(get_engineering_data())

def start_server():
    app.run(host=Config.HOST, port=Config.PORT)