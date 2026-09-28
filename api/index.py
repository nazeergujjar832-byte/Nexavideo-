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

            opts = {
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'web']
                    }
                },
                'extractor_retries': 3,
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
                if not video_url:
                    fmts = info.get('formats', [])
                    # best mp4 dhoondo
                    best = None
                    for f in reversed(fmts):
                        if f.get('ext') == 'mp4' and f.get('url'):
                            best = f.get('url')
                            break
                    video_url = best or (fmts[-1].get('url') if fmts else None)

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
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
