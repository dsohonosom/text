#!/usr/bin/env python3
"""Simple command-line idea tracker."""
import sys
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


def add_idea(text):
    data = load_data()
    data.append({"idea": text, "timestamp": datetime.now().isoformat(timespec="seconds")})
    save_data(data)
    print("Idea added.")


def list_ideas():
    data = load_data()
    if not data:
        print("No ideas recorded.")
        return
    for i, item in enumerate(data, 1):
        print(f"{i}. {item['idea']} ({item['timestamp']})")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: idea.py add <idea> | list")
        return
    if argv[0] == "add":
        if len(argv) < 2:
            print("Please provide an idea text.")
        else:
            add_idea(" ".join(argv[1:]))
    elif argv[0] == "list":
        list_ideas()
    else:
        print(f"Unknown command: {argv[0]}")


if __name__ == "__main__":
    main()
