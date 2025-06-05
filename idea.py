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


class IdeaHandler(http.server.BaseHTTPRequestHandler):
    """Simple request handler to display and update ideas."""

    def _render_page(self, message=""):
        ideas = load_data()
        html = [
            "<html><head><meta charset='utf-8'><title>Idea Tracker</title></head><body>",
            "<h1>Idea Tracker</h1>",
        ]
        if message:
            html.append(f"<p>{message}</p>")
        today = datetime.now().strftime("%Y-%m-%d")
        html.append(
            "<form method='post' action='/add'>"
            "Idea: <input type='text' name='idea' size='40'/> "
            f"Date: <input type='date' name='date' value='{today}'/> "
            "Done: <input type='checkbox' name='done'/> "
            "<input type='submit' value='Add Idea'/></form>"
        )
        html.append("<h2>Ideas</h2><ul>")
        if not ideas:
            html.append("<li>No ideas recorded.</li>")
        else:
            for item in ideas:
                done_flag = "✓" if item.get("done") else "x"
                date = item.get("date", "-")
                html.append(f"<li>{item['idea']} [{date}] ({done_flag})</li>")
        html.append("</ul></body></html>")
        body = "".join(html).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._render_page()
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
                message = "Idea added."
            else:
                message = "No idea provided."
            self._render_page(message)
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
    subparsers.add_parser("gui", help="Launch web GUI")

    args = parser.parse_args(argv)

    if args.command == "add":
        add_idea(" ".join(args.text), date=args.date, done=args.done)
    elif args.command == "list":
        list_ideas()
    elif args.command == "gui":
        show_gui()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
