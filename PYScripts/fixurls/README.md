# fixurls.py

## Description
Cleans up junk characters and metadata artifacts (like duration tags or backslashes) from URLs in the `scene_urls` table of a Stash SQLite database using Regex.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Ensure `stash-go.sqlite` is in the same directory as the script or update the `sqlite3.connect` path.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python fixurls.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.