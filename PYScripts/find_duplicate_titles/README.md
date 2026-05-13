# find_duplicate_titles.py

## Description
A utility to identify duplicate scene titles in a Stash database and output only the titles themselves to a text file. Useful for manual cleanup planning.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Update the `db_path` and `output_file` variables at the bottom of the script.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python find_duplicate_titles.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.