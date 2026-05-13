# joinmp4s.py

## Description
Safely concatenates multiple MP4 files. It standardizes segments into MPEG-TS format using NVENC (NVIDIA GPU) acceleration before stitching them to ensure perfect sync and compatibility.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Place the script in the folder containing the MP4s you want to join. Requires an NVIDIA GPU for `hevc_nvenc` support.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python joinmp4s.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.