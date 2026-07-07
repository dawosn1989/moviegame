import http.server
import json
import os

PORT = 8005
LEADERBOARD_FILE = "leaderboard.json"

# Initialize file as a list of scores instead of a single object
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump([
            {"initials": "AAA", "score": 3000},
            {"initials": "BBB", "score": 2000},
            {"initials": "CCC", "score": 1000}
        ], f, indent=4)

class GameServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.split('?')[0].rstrip('/')
        
        # HTML Leaderboard Page Route
        if clean_path == "/leaderboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            with open(LEADERBOARD_FILE, "r") as f:
                scores = json.load(f)
            
            # Dynamically build table rows for the Top 3
            rows_html = ""
            for idx, entry in enumerate(scores[:3], start=1):
                rows_html += f"""
                <tr>
                    <td>#{idx}</td>
                    <td>{entry.get('initials', '---')}</td>
                    <td>{entry.get('score', 0)}</td>
                </tr>
                """

            html_page = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Cinema Riddle Throne Room</title>
                <style>
                    body {{ font-family: 'Segoe UI', sans-serif; background: #111; color: #fff; text-align: center; padding-top: 50px; }}
                    .box {{ background: #000; border: 2px solid #ffcc00; display: inline-block; padding: 40px; border-radius: 12px; box-shadow: 0 0 20px #ffcc0044; }}
                    h1 {{ color: #ffcc00; margin-bottom: 5px; letter-spacing: 2px; }}
                    p {{ color: #aaa; font-size: 1.2rem; margin-bottom: 25px; }}
                    table {{ width: 100%; border-collapse: collapse; font-size: 1.5rem; margin: 20px 0; font-family: monospace; }}
                    td, th {{ padding: 12px 25px; text-align: center; }}
                    th {{ color: #ffcc00; border-bottom: 2px solid #333; }}
                    tr:nth-child(1) td {{ color: #00e676; font-weight: bold; font-size: 1.8rem; }}
                    .btn {{ display: inline-block; margin-top: 20px; color: #ffcc00; text-decoration: none; border: 1px solid #ffcc00; padding: 8px 16px; border-radius: 4px; }}
                    .btn:hover {{ background: #ffcc00; color: #000; }}
                </style>
            </head>
            <body>
                <div class="box">
                    <h1>ARCADE HALL OF FAME</h1>
                    <p>Top 3 Dynamic High Scores</p>
                    <table>
                        <tr>
                            <th>RANK</th>
                            <th>NAME</th>
                            <th>SCORE</th>
                        </tr>
                        {rows_html}
                    </table>
                    <a class="btn" href="/">Return to Game</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_page.encode("utf-8"))
            
        # API Endpoint to fetch scores
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
            new_entry = json.loads(post_data.decode("utf-8"))
            
            # Load existing scores list
            if os.path.exists(LEADERBOARD_FILE):
                with open(LEADERBOARD_FILE, "r") as f:
                    scores = json.load(f)
                    if not isinstance(scores, list): scores = []
            else:
                scores = []

            # Append the fresh entry, sort descending by score value, and keep top 10 logs
            scores.append(new_entry)
            scores.sort(key=lambda x: x.get('score', 0), reverse=True)
            scores = scores[:10] 
            
            with open(LEADERBOARD_FILE, "w") as f:
                json.dump(scores, f, indent=4)
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

print(f"Serving permanent leaderboard engine at http://localhost:{PORT}")
http.server.HTTPServer(("0.0.0.0", PORT), GameServer).serve_forever()