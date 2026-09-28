from http.server import BaseHTTPRequestHandler
import json
import yt_dlp
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            video_url = query.get('url', [None])[0]

            if not video_url:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error":"No URL"}).encode())
                return

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                formats = []
                for f in info.get('formats', [])[-10:]:
                    if f.get('url'):
                        formats.append({
                            "quality": f.get('format_note') or f.get('height'),
                            "ext": f.get('ext'),
                            "url": f.get('url')
                        })

                result = {
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "formats": formats,
                    "direct_url": info.get('url')
                }

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
