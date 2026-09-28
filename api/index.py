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
        video_url = query.get('url', [None])[0]

        # Agar URL nahi diya to status dikhao
        if not video_url:
            data = {
                "status": "Nexavideo API is Running!",
                "creator": "Nazeer Gujjar",
                "usage": "/api/index.py?url=YOUTUBE_OR_TIKTOK_LINK"
            }
            self.wfile.write(json.dumps(data).encode())
            return

        # Downloader logic
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

                response = {
                    "status": "success",
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "duration": info.get('duration'),
                    "url": info.get('url'), # direct link
                    "ext": info.get('ext'),
                    "all_formats": len(info.get('formats', []))
                }
                self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            error = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(error).encode())
