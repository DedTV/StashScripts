# TitleCase.py

## Description
Connects to a Stash SQLite database to scan all scene titles and convert them to proper 'Smart' Title Case using a library. Includes a custom abbreviation list (USA, UK, etc.) to maintain correct acronym capitalization.

## Requirements
- Python 3.x (or PowerShell for .ps1 files)
- Access to the relevant media or database files.

## Configuration & Usage
Requires the `titlecase` library (`pip install titlecase`). Update `DATABASE_FILE` and modify the `custom_abbreviations` list as needed.

1. Open the file in a text editor.
2. Locate the configuration section at the top.
3. Modify the paths and variables to match your environment.
4. Run the script: `python TitleCase.py` (or `powershell ./TitleCase.py`)

## Notes
- **Safety First**: Always back up your `stash-go.sqlite` database before running any script that modifies data.
- **Hardware Acceleration**: Scripts using NVENC require an NVIDIA GPU and compatible FFmpeg build.