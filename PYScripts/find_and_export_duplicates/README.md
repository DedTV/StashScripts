# find_and_export_duplicates.py

## Description
Connects to a Stash SQLite database and identifies scenes with identical titles. Exports the ID and Title of duplicate records to a tab-separated text file.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Update `DATABASE_PATH` and `OUTPUT_PATH` constants at the top of the file.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python find_and_export_duplicates.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.