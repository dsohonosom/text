# Idea Tracker

This repository provides a simple command-line tool for jotting down ideas and
reviewing them later. A small web interface is also available.

## Usage

### 1. Add an idea

   ```bash
   python3 idea.py add "my cool idea" --date 2023-01-01 --done
   ```
   The `--date` option sets the idea's date (defaults to today). Use `--done` to
   mark that the idea has already been considered or implemented.

### 2. List saved ideas

   ```bash
   python3 idea.py list
   ```
   Each idea is printed with its date and whether it has been done (`✓` for done,
   `x` for not yet).

### 3. Mark an idea as done

   ```bash
   python3 idea.py done 1
   ```
   The number is the idea's position from the `list` command.

### 4. Use the GUI

   ```bash
   python3 idea.py gui
   ```
   Launches a local web server and opens your browser to
   `http://localhost:8000`. The interface is in Japanese and the form is
   centered on the page.

Ideas are stored locally in `ideas.json`. This file is ignored by Git.
