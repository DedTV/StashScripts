# trimscrapers.py

## Description
Scans a community scraper directory to identify folders where *none* of the contained files contain any Top-Level Domains (TLDs) from a provided list. Useful for filtering out scrapers that don't point to external URLs.

## Requirements
- Python 3.x (or PowerShell for .ps1 files)
- Access to the relevant media or database files.

## Configuration & Usage
Set `TLD_INPUT` (path to a text file with one TLD per line), `SEARCH_ROOT` (your scrapers folder), and `RESULT_OUTPUT` (where to save the folder list).

1. Open the file in a text editor.
2. Locate the configuration section at the top.
3. Modify the paths and variables to match your environment.
4. Run the script: `python trimscrapers.py` (or `powershell ./trimscrapers.py`)

## Notes
- **Safety First**: Always back up your `stash-go.sqlite` database before running any script that modifies data.
- **Hardware Acceleration**: Scripts using NVENC require an NVIDIA GPU and compatible FFmpeg build.