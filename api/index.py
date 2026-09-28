from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api', methods=['GET'])
@app.route('/api/index.py', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "ok", "message": "NexaVideo API is Live! Use ?url="})

    try:
        ydl_opts = {'quiet': True, 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info.get('url')
            if not download_url:
                download_url = info['formats'][-1]['url']
            
            return jsonify({
                "status": "success",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "download_url": download_url
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
