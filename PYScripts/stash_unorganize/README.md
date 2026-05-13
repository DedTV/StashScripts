# stash_unorganize.py

## Description
Prepares a Stash library for the 'Identify' task by backing up currently organized scene IDs into a temporary table and then setting their status to 'Unorganized' (0). This ensures they are picked up by the identification process.

## Requirements
- Python 3.x (or PowerShell for .ps1 files)
- Access to the relevant media or database files.

## Configuration & Usage
Ensure `DB_PATH` points to your `stash-go.sqlite` file. Run this *before* running the Stash 'Identify' task.

1. Open the file in a text editor.
2. Locate the configuration section at the top.
3. Modify the paths and variables to match your environment.
4. Run the script: `python stash_unorganize.py` (or `powershell ./stash_unorganize.py`)

## Notes
- **Safety First**: Always back up your `stash-go.sqlite` database before running any script that modifies data.
- **Hardware Acceleration**: Scripts using NVENC require an NVIDIA GPU and compatible FFmpeg build.