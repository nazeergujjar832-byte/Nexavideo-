from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "Nexavideo API is Running!",
            "creator": "Nazeer Gujjar - LIVE",
            "message": "Mubarak ho API live ho gayi!"
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
