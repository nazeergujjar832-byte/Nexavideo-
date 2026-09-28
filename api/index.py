from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        data = {"status": "Nexavideo API is Running!", "creator": "Nazeer Gujjar"}
        self.wfile.write(json.dumps(data).encode())
