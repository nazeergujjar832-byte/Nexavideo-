from http.server import BaseHTTPRequestHandler
import json, yt_dlp
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            qs = parse_qs(urlparse(self.path).query)
            url = qs.get('url', [None])[0]
            if not url:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(b'{"error":"URL missing"}')
                return

            # FIX: format nahi likhna, yt-dlp khud best le lega
            opts = {
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # direct best url
                video_url = info.get('url')
                # agar url na mile to formats me se best lo
                if not video_url:
                    fmts = info.get('formats', [])
                    if fmts:
                        video_url = fmts[-1].get('url')

                data = {
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "url": video_url
                }

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
