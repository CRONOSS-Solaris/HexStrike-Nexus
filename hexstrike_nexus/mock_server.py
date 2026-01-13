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

        if self.path == '/api/logs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            logs = [
                f"[INFO] {time.strftime('%H:%M:%S')} - Scanning port {random.randint(1, 65535)}",
                f"[DEBUG] {time.strftime('%H:%M:%S')} - Worker thread started",
                f"[INFO] {time.strftime('%H:%M:%S')} - Nuclei scan in progress...",
                f"[WARN] {time.strftime('%H:%M:%S')} - Rate limiting detected"
            ] if random.random() > 0.3 else []
            self.wfile.write(json.dumps({"logs": logs}).encode('utf-8'))
            return

        if self.path == '/api/cache/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            stats = {
                "hits": random.randint(1000, 5000),
                "misses": random.randint(10, 100),
                "size_mb": round(random.uniform(10.0, 500.0), 2)
            }
            self.wfile.write(json.dumps(stats).encode('utf-8'))
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

        if self.path.startswith('/api/processes/terminate/'):
            pid = self.path.split('/')[-1]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "terminated", "pid": pid}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def run_server():
    # Bind to localhost for security
    with ReusableTCPServer(("127.0.0.1", PORT), HexStrikeHandler) as httpd:
        print(f"Serving Mock HexStrike Server on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
