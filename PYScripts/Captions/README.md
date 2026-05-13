# Captions.py

## Description
Generates SRT subtitles for video files using the `faster-whisper` model. It translates audio to English and groups words into short, readable chunks. Includes a 10-minute timeout per file to prevent hangs.

## Requirements
- Python 3.x
- Access to the relevant media or database files.

## Configuration & Usage
Update `SOURCE_DIR`, `MODEL_SIZE` (e.g., 'large-v3'), and `DEVICE` (e.g., 'cuda' or 'cpu'). Requires `faster-whisper` and a GPU for optimal performance.

1. Open the script in a text editor.
2. Locate the configuration section at the top (usually marked with `--- CONFIGURATION ---`).
3. Modify the paths and variables to match your environment.
4. Run the script: `python Captions.py`

## Notes
- Always back up your database (SQLite files) before running scripts that perform `UPDATE` or `DELETE` operations.
- Ensure FFmpeg is installed and added to your system PATH if the script references it.