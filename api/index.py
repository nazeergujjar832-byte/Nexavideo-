from http.server import BaseHTTPRequestHandler
import json, requests
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

            # Cobalt API use karo - ye bot block nahi hota
            api_url = "https://api.cobalt.tools/api/json"
            payload = {"url": url, "vQuality": "720", "vCodec": "h264"}
            headers = {"Accept": "application/json", "Content-Type": "application/json"}

            r = requests.post(api_url, json=payload, headers=headers, timeout=30)
            data_cobalt = r.json()

            if data_cobalt.get('status') == 'error':
                raise Exception(data_cobalt.get('text', 'Cobalt error'))

            video_url = data_cobalt.get('url')
            if not video_url:
                raise Exception("Video not found, try another link")

            result = {
                "title": "Video Ready - NEXAVIDEO",
                "thumbnail": "",
                "url": video_url
            }

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
