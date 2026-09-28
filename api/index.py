from http.server import BaseHTTPRequestHandler
import json, yt_dlp
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            url = query.get('url', [None])[0]

            if not url:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(b'{"error":"Link nahi diya"}')
                return

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'web']
                    }
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'NEXAVIDEO')
                thumb = info.get('thumbnail', '')

                # best mp4 url
                video_url = info.get('url')
                if not video_url:
                    formats = info.get('formats', [])
                    for f in reversed(formats):
                        if f.get('vcodec')!= 'none' and f.get('acodec')!= 'none' and f.get('ext') == 'mp4':
                            video_url = f.get('url')
                            break
                    if not video_url and formats:
                        video_url = formats[-1].get('url')

                data = {
                    "title": title,
                    "thumbnail": thumb,
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
