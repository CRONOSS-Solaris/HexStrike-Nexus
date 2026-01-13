import http.server
import socketserver
import json
import time
import random
import threading

PORT = 8888

class HexStrikeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "OK"}')
            return

        if self.path == '/api/telemetry':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            telemetry = {
                "cpu_usage": random.randint(10, 60),
                "ram_usage": random.randint(20, 80),
                "cache_hits": random.randint(100, 5000),
                "active_processes": [
                    {"pid": 4021, "name": "masscan", "status": "running"},
                    {"pid": 4025, "name": "nuclei", "status": "running"}
                ] if random.random() > 0.5 else []
            }
            self.wfile.write(json.dumps(telemetry).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == '/api/intelligence/analyze-target':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            target = data.get('target', 'unknown')
            response = {
                "status": "success",
                "plan": [
                    f"Initiating recon on {target}",
                    "Checking DNS records...",
                    "Enumerating subdomains...",
                    "Scanning for open ports..."
                ],
                "agent": "BugBountyWorkflowManager"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        if self.path == '/api/intelligence/select-tools':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "tools": ["subfinder", "nuclei", "httpx"],
                "reasoning": "Standard web reconnaissance workflow selected."
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def run_server():
    with ReusableTCPServer(("", PORT), HexStrikeHandler) as httpd:
        print(f"Serving Mock HexStrike Server on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
