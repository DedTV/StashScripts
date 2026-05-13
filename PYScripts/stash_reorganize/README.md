# stash_reorganize.py

## Description
Restores the 'Organized' status of scenes in a Stash database using a temporary tracker table. It specifically targets scenes previously marked as 0 (unorganized) that are present in the `tmp_organized_tracker` table, then cleans up the tracker.

## Requirements
- Python 3.x (or PowerShell for .ps1 files)
- Access to the relevant media or database files.

## Configuration & Usage
Ensure `DB_PATH` points to your `stash-go.sqlite` file. Run this *after* your identification/reorganization work is complete to restore the status.

1. Open the file in a text editor.
2. Locate the configuration section at the top.
3. Modify the paths and variables to match your environment.
4. Run the script: `python stash_reorganize.py` (or `powershell ./stash_reorganize.py`)

## Notes
- **Safety First**: Always back up your `stash-go.sqlite` database before running any script that modifies data.
- **Hardware Acceleration**: Scripts using NVENC require an NVIDIA GPU and compatible FFmpeg build.