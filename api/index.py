from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "Nexavideo API is Running!", "creator": "Nazeer Gujjar - LIVE"})

@app.route('/api/video')
def video():
    return jsonify({"message": "API is live, now adding downloader"})
