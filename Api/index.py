from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import yt_dlp

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        url = query.get('url', [None])[0]

        # agar url nahi diya to status dikhao
        if not url:
            data = {"status": "Nexavideo API is Running!", "creator": "Nazeer Gujjar"}
            self.wfile.write(json.dumps(data).encode())
            return

        try:
            ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                result = {
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "duration": info.get('duration'),
                    "video_url": info.get('url'),
                    "formats": info.get('formats')[-5:]
                }
                self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.wfile.write(json.dumps({"error": str(e)}).encode())
