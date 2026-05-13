# clipsT.py

## Description
Traverses a directory to find MP4s and automatically cuts them into segments of a specified duration (default 45 seconds) using `moviepy`.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Edit the `traverse_and_cut_videos` call at the bottom of the script with your source and destination paths.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python clipsT.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.