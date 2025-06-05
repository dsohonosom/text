#!/usr/bin/env python3
"""Simple command-line idea tracker."""
import argparse
import os
import json
from datetime import datetime

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


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple command-line idea tracker")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new idea")
    add_p.add_argument("text", nargs="+", help="Idea text")
    add_p.add_argument("--date", "-d", help="Date for the idea (YYYY-MM-DD)")
    add_p.add_argument("--done", action="store_true", help="Mark idea as considered/implemented")

    subparsers.add_parser("list", help="List saved ideas")

    args = parser.parse_args(argv)

    if args.command == "add":
        add_idea(" ".join(args.text), date=args.date, done=args.done)
    elif args.command == "list":
        list_ideas()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
