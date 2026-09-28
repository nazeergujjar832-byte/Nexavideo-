from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import yt_dlp

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            qs = parse_qs(parsed.query)
            video_url = qs.get('url', [None])[0]

            if not video_url:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": "API Running! Use?url=YOUTUBE_LINK"}).encode())
                return

            ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                best_url = info.get('url')
                if not best_url and info.get('formats'):
                    best_url = info['formats'][-1]['url']

                result = {
                    "status": "success",
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "download_url": best_url
                }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
