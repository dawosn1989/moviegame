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
        clean_path = self.path.split('?')[0].rstrip('/')
        
        # 1. NEW: Direct Browser URL to check the high score throne room
        if clean_path == "/leaderboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
            
            html_page = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Cinema Riddle Throne Room</title>
                <style>
                    body {{ font-family: 'Segoe UI', sans-serif; background: #111; color: #fff; text-align: center; padding-top: 50px; }}
                    .box {{ background: #000; border: 2px solid #ffcc00; display: inline-block; padding: 40px; border-radius: 12px; box-shadow: 0 0 20px #ffcc0044; }}
                    h1 {{ color: #ffcc00; margin-bottom: 5px; letter-spacing: 2px; }}
                    h2 {{ color: #00e676; font-size: 3rem; margin: 20px 0; font-family: monospace; }}
                    p {{ color: #aaa; font-size: 1.2rem; }}
                    .btn {{ display: inline-block; margin-top: 20px; color: #ffcc00; text-decoration: none; border: 1px solid #ffcc00; padding: 8px 16px; border-radius: 4px; }}
                    .btn:hover {{ background: #ffcc00; color: #000; }}
                </style>
            </head>
            <body>
                <div class="box">
                    <h1>CURRENT CHAMPION</h1>
                    <p>All-Time High Score Record</p>
                    <h2>{data.get('initials', '---')} - {data.get('score', 0)} pts</h2>
                    <a class="btn" href="/">Return to Game</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_page.encode("utf-8"))
            
        # 2. API Endpoint to fetch the current global high score data
        elif clean_path == "/api/leaderboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            with open(LEADERBOARD_FILE, "r") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        clean_path = self.path.split('?')[0].rstrip('/')
        if clean_path == "/api/leaderboard":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_record = json.loads(post_data.decode("utf-8"))
            
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