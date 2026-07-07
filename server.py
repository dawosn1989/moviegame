import http.server
import json
import os

PORT = 8005
LEADERBOARD_FILE = "leaderboard.json"

# Ensure the leaderboard storage file exists with a default baseline
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump({"initials": "AAA", "score": 0}, f)

class GameServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Clean up the path to strip out hostnames or trailing parameters
        clean_path = self.path.split('?')[0].rstrip('/')
        
        # API Endpoint to fetch the current global high score
        if clean_path == "/api/leaderboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            
            with open(LEADERBOARD_FILE, "r") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            # Serve regular assets (index.html, JSON, images)
            super().do_GET()

    def do_POST(self):
        clean_path = self.path.split('?')[0].rstrip('/')
        
        # API Endpoint to save a new record permanently
        if clean_path == "/api/leaderboard":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_record = json.loads(post_data.decode("utf-8"))
            
            # Save to disk permanently
            with open(LEADERBOARD_FILE, "w") as f:
                json.dump(new_record, f, indent=4)
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

print(f"Serving permanent leaderboard engine at http://localhost:{PORT}")
http.server.HTTPServer(("0.0.0.0", PORT), GameServer).serve_forever()