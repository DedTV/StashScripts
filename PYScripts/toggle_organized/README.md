# toggle_organized.py

## Description
A debug-friendly utility that toggles scenes between Organized and Unorganized states. If a tracker exists, it reverts scenes to organized; if not, it backs up organized IDs and sets them to 0. Includes extensive logging for troubleshooting.

## Requirements
- Python 3.x (or PowerShell for .ps1 files)
- Access to the relevant media or database files.

## Configuration & Usage
Verify the `DB_PATH` variable. This script is intended for testing and manual recovery of the organized status.

1. Open the file in a text editor.
2. Locate the configuration section at the top.
3. Modify the paths and variables to match your environment.
4. Run the script: `python toggle_organized.py` (or `powershell ./toggle_organized.py`)

## Notes
- **Safety First**: Always back up your `stash-go.sqlite` database before running any script that modifies data.
- **Hardware Acceleration**: Scripts using NVENC require an NVIDIA GPU and compatible FFmpeg build.