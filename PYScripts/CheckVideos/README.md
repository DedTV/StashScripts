# CheckVideos.py

## Description
A multiprocessing-capable video integrity checker. It uses FFmpeg to probe files for errors, maintaining a progress log to resume interrupted scans and a 'bad files' list for easy identification of broken media.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Adjust `ROOT_DIR` to your media path and `MAX_WORKERS` to match your CPU core count.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python CheckVideos.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.