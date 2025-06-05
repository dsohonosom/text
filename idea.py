#!/usr/bin/env python3
"""Simple command-line idea tracker."""
import argparse
import os
import json
from datetime import datetime
import http.server
import socketserver
import urllib.parse
import webbrowser

DATA_FILE = "ideas.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_idea(text, date=None, done=False):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    data = load_data()
    data.append(
        {
            "idea": text,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "date": date,
            "done": done,
        }
    )
    save_data(data)
    print("Idea added.")


def list_ideas():
    data = load_data()
    if not data:
        print("No ideas recorded.")
        return
    for i, item in enumerate(data, 1):
        done_flag = "✓" if item.get("done") else "x"
        date = item.get("date", "-")
        print(f"{i}. {item['idea']} [{date}] ({done_flag})")


def mark_done(index):
    """Mark an existing idea as done by its index (0-based)."""
    data = load_data()
    if 0 <= index < len(data):
        data[index]["done"] = True
        save_data(data)
        print(f"Idea {index + 1} marked as done.")
    else:
        print("Invalid idea index.")


class IdeaHandler(http.server.BaseHTTPRequestHandler):
    """Simple request handler serving a small HTML/JS interface."""

    def _send_file(self, path, ctype):
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self._send_file("index.html", "text/html; charset=utf-8")
        elif self.path == "/style.css":
            self._send_file("style.css", "text/css; charset=utf-8")
        elif self.path == "/script.js":
            self._send_file("script.js", "application/javascript; charset=utf-8")
        elif self.path == "/ideas":
            data = json.dumps(load_data()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/add":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length).decode()
            params = urllib.parse.parse_qs(data)
            text = params.get("idea", [""])[0].strip()
            date = params.get("date", [""])[0] or None
            done = "done" in params
            if text:
                add_idea(text, date=date, done=done)
            self.send_response(204)
            self.end_headers()
        elif self.path == "/done":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length).decode()
            params = urllib.parse.parse_qs(data)
            idx = int(params.get("idx", ["-1"])[0])
            mark_done(idx)
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404)


def show_gui(host="127.0.0.1", port=8000):
    """Start a simple HTTP server and open a browser for interaction."""
    with socketserver.TCPServer((host, port), IdeaHandler) as httpd:
        url = f"http://{host}:{port}/"
        print(f"Serving on {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        httpd.serve_forever()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple command-line idea tracker")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new idea")
    add_p.add_argument("text", nargs="+", help="Idea text")
    add_p.add_argument("--date", "-d", help="Date for the idea (YYYY-MM-DD)")
    add_p.add_argument("--done", action="store_true", help="Mark idea as considered/implemented")

    subparsers.add_parser("list", help="List saved ideas")
    gui_p = subparsers.add_parser("gui", help="Launch web GUI")
    gui_p.add_argument("--host", default="127.0.0.1", help="Host to serve on")
    gui_p.add_argument("--port", type=int, default=8000, help="Port to serve on")
    done_p = subparsers.add_parser("done", help="Mark idea as done")
    done_p.add_argument("index", type=int, help="Idea number (1-based)")

    args = parser.parse_args(argv)

    if args.command == "add":
        add_idea(" ".join(args.text), date=args.date, done=args.done)
    elif args.command == "list":
        list_ideas()
    elif args.command == "gui":
        show_gui(host=args.host, port=args.port)
    elif args.command == "done":
        mark_done(args.index - 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
