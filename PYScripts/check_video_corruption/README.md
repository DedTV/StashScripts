# check_video_corruption.py

## Description
Scans a directory for MP4 files and uses FFmpeg with CUDA hardware acceleration to detect stream corruption or decoding errors. Outputs results to a CSV and logs detailed errors.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Requires FFmpeg with CUDA support. The script prompts for the directory path upon execution.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python check_video_corruption.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.