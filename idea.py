#!/usr/bin/env python3
"""Simple command-line idea tracker."""
import argparse
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

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


def show_gui():
    root = tk.Tk()
    root.title("Idea Tracker")

    tk.Label(root, text="Idea:").grid(row=0, column=0, sticky="e")
    idea_entry = tk.Entry(root, width=40)
    idea_entry.grid(row=0, column=1, columnspan=3, sticky="we")

    tk.Label(root, text="Date:").grid(row=1, column=0, sticky="e")
    date_entry = tk.Entry(root)
    date_entry.grid(row=1, column=1, sticky="we")
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    done_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Done", variable=done_var).grid(row=1, column=2, sticky="w")

    status_var = tk.StringVar()
    tk.Label(root, textvariable=status_var).grid(row=2, column=0, columnspan=4, sticky="w")

    def on_add():
        text = idea_entry.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Please enter an idea.")
            return
        add_idea(text, date=date_entry.get().strip(), done=done_var.get())
        status_var.set("Idea added.")
        idea_entry.delete(0, tk.END)
        show_list()

    tk.Button(root, text="Add Idea", command=on_add).grid(row=3, column=0, sticky="we")

    ideas_box = tk.Text(root, width=60, height=10, state="disabled")
    ideas_box.grid(row=4, column=0, columnspan=4, pady=(5, 0))

    def show_list():
        ideas = load_data()
        ideas_box.config(state="normal")
        ideas_box.delete("1.0", tk.END)
        if not ideas:
            ideas_box.insert(tk.END, "No ideas recorded.\n")
        else:
            for i, item in enumerate(ideas, 1):
                done_flag = "✓" if item.get("done") else "x"
                date = item.get("date", "-")
                ideas_box.insert(tk.END, f"{i}. {item['idea']} [{date}] ({done_flag})\n")
        ideas_box.config(state="disabled")

    tk.Button(root, text="List Ideas", command=show_list).grid(row=3, column=1, sticky="we")

    show_list()
    root.mainloop()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple command-line idea tracker")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new idea")
    add_p.add_argument("text", nargs="+", help="Idea text")
    add_p.add_argument("--date", "-d", help="Date for the idea (YYYY-MM-DD)")
    add_p.add_argument("--done", action="store_true", help="Mark idea as considered/implemented")

    subparsers.add_parser("list", help="List saved ideas")
    subparsers.add_parser("gui", help="Launch GUI")

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
