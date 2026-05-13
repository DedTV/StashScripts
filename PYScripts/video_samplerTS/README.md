# video_samplerTS.py

## Description
A Stash plugin script that generates standardized 30-second .ts clips at specific points (50%, 75%, 90%) of a video's duration. It uses NVENC for high-speed hardware-accelerated transcoding to 1080p, optimized for gapless joining.

## Requirements
- Python 3.x (or PowerShell for .ps1 files)
- Access to the relevant media or database files.

## Configuration & Usage
Requires `stashapi`. Update `FFMPEG_PATH`, `FFPROBE_PATH`, and `OUTPUT_DIR`. Designed to run as a Stash plugin via the associated .yml file.

1. Open the file in a text editor.
2. Locate the configuration section at the top.
3. Modify the paths and variables to match your environment.
4. Run the script: `python video_samplerTS.py` (or `powershell ./video_samplerTS.py`)

## Notes
- **Safety First**: Always back up your `stash-go.sqlite` database before running any script that modifies data.
- **Hardware Acceleration**: Scripts using NVENC require an NVIDIA GPU and compatible FFmpeg build.