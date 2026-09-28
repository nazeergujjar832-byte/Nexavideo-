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
        query = urlparse(self.path).query
        params = parse_qs(query)
        url = params.get('url', [None])[0]
        if not url:
            self.wfile.write(json.dumps({"status":"ok", "message":"API is Running"}).encode())
            return
        try:
            ydl_opts = {'quiet': True, 'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                data = {
                    "status": "success",
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "download_url": info.get('url') or info['formats'][-1]['url']
                }
                self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            self.wfile.write(json.dumps({"status":"error", "message": str(e)}).encode())
