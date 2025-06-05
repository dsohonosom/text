#!/usr/bin/env python3
"""Simple GUI-based idea tracker using Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
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


def list_ideas():
    return load_data()


def main():
    root = tk.Tk()
    root.title("Idea Tracker")

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    idea_var = tk.StringVar()

    entry = ttk.Entry(frame, textvariable=idea_var, width=40)
    entry.grid(row=0, column=0, padx=(0, 5))

    listbox = tk.Listbox(frame, width=60)
    listbox.grid(row=1, column=0, columnspan=2, pady=(10, 0))

    def refresh():
        listbox.delete(0, tk.END)
        for i, item in enumerate(list_ideas(), 1):
            listbox.insert(tk.END, f"{i}. {item['idea']} ({item['timestamp']})")

    def add():
        text = idea_var.get().strip()
        if not text:
            messagebox.showinfo("Input required", "Please enter an idea.")
            return
        add_idea(text)
        idea_var.set("")
        refresh()

    add_button = ttk.Button(frame, text="Add Idea", command=add)
    add_button.grid(row=0, column=1)

    refresh()
    root.mainloop()


if __name__ == "__main__":
    main()
