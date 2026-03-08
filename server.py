#!/usr/bin/env python3
"""
Wedding RSVP Server
-------------------
Run:  python server.py
Then open:  http://localhost:8000

Guest data is saved automatically to guests.json in this folder.
"""

import json, os, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

GUESTS_FILE = os.path.join(os.path.dirname(__file__), "guests.json")
PORT = int(os.environ.get("PORT", 8000))


def load_guests():
    if not os.path.exists(GUESTS_FILE):
        return []
    with open(GUESTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_guests(data):
    with open(GUESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Handler(SimpleHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()}  {fmt % args}")

    def do_GET(self):
        # Serve wedding-invite.html as the homepage
        if self.path == "/" or self.path == "":
            self.path = "/wedding-invite.html"
            return super().do_GET()
        elif self.path == "/api/guests":
            self._json(200, load_guests())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/guests":
            body = self._read_body()
            entry = json.loads(body)
            guests = load_guests()
            guests.append(entry)
            save_guests(guests)
            print(f"  ✦ New RSVP saved → {entry.get('fullName', '?')}")
            self._json(200, {"ok": True, "total": len(guests)})
        else:
            self._json(404, {"error": "not found"})

    def do_DELETE(self):
        if self.path.startswith("/api/guests/"):
            gid = self.path.split("/")[-1]
            guests = load_guests()
            before = len(guests)
            guests = [g for g in guests if g.get("id") != gid]
            save_guests(guests)
            removed = before - len(guests)
            print(f"  ✦ Deleted guest id={gid}  (removed {removed})")
            self._json(200, {"ok": True, "removed": removed})
        else:
            self._json(404, {"error": "not found"})

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode("utf-8")

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code, data):
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    if not os.path.exists(GUESTS_FILE):
        save_guests([])
        print(f"  Created guests.json")

    server = HTTPServer(("", PORT), Handler)
    print(f"\n  ╔══════════════════════════════════════════╗")
    print(f"  ║  Wedding RSVP Server  →  running         ║")
    print(f"  ║  Port: {PORT}                               ║")
    print(f"  ╚══════════════════════════════════════════╝\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        sys.exit(0)
