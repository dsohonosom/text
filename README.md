# Idea Tracker

This repository provides a minimal command-line tool for jotting down ideas and
reviewing them later.

## Usage

1. **Add an idea**

   ```bash
   python3 idea.py add "my cool idea" --date 2023-01-01 --done
   ```
   The `--date` option sets the idea's date (defaults to today). Use `--done` to
   mark that the idea has already been considered or implemented.

2. **List saved ideas**

   ```bash
   python3 idea.py list
   ```
   Each idea is printed with its date and whether it has been done (`✓` for done,
   `x` for not yet).

Ideas are stored locally in `ideas.json`. This file is ignored by Git.
