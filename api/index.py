from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "Nexavideo API is Running!", "creator": "Nazeer Gujjar"})

@app.route('/api/video')
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "url missing"}), 400
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "video_url": info.get('url')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
