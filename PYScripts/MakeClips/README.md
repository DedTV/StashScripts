# MakeClips.py

## Description
Creates three 10-second preview samples (at 50%, 75%, and 90% of the duration) for MP4 videos in a source directory. Uses stream copying for near-instant processing without quality loss.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Update `FFMPEG_PATH`, `FFPROBE_PATH`, `SOURCE_DIR`, and `OUTPUT_DIR`. Adjust the `file_limit` variable if you wish to process more than 5 files.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python MakeClips.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.