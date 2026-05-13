# foldercheck.py

## Description
Identifies 'Studios' in a Stash database that lack a corresponding entry in the 'folders' table. Useful for diagnosing organization/mapping issues after library moves.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Update `DB_PATH` and `OUTPUT_CSV` constants at the top of the file.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python foldercheck.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.