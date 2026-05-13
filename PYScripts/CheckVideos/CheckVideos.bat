@echo off
setlocal EnableDelayedExpansion

REM Set the root directory to search
SET "ROOT_DIR=F:\Stashed\CaughtFapping"

REM Set the log file path
SET "LOG_FILE=error.log"
REM Set a temporary file for individual errors
SET "TEMP_ERR=__temp_err.log"
REM Set a file to track progress for resuming
SET "PROGRESS_FILE=processed_files.log"

REM Setup logs
IF NOT EXIST "!PROGRESS_FILE!" (
    ECHO Starting fresh scan...
    IF EXIST "!LOG_FILE!" DEL "!LOG_FILE!"
) ELSE (
    ECHO Resuming from previous scan...
)

ECHO Starting video probe using ffmpeg (null output method)...
ECHO Probing files in !ROOT_DIR! and its subdirectories.
ECHO Errors will be logged to !LOG_FILE!

REM Iterate recursively through the directory
FOR /R "%ROOT_DIR%" %%F IN (*.mp4) DO (
    
    REM Store the filename in a variable safe for Delayed Expansion
    SET "FULLPATH=%%F"
    
    REM Check if file is already in the progress log
    REM /L = Literal, /I = Case Insensitive (fixes drive letter case issues), /C = Exact String
    findstr /L /I /C:"!FULLPATH!" "!PROGRESS_FILE!" >nul 2>&1
    
    REM If errorlevel 1, the file was NOT found in the log
    IF ERRORLEVEL 1 (
        ECHO Probing: "!FULLPATH!"
        
        REM Delete the temp error file before each run
        IF EXIST "!TEMP_ERR!" (
            DEL "!TEMP_ERR!"
        )
        
        REM Run ffmpeg
        REM We use quotes around the path to handle spaces
        ffmpeg -v error -i "!FULLPATH!" -f null - 2>"!TEMP_ERR!"
        
        REM Check if the temp error file has a size greater than 0
        FOR %%T IN ("!TEMP_ERR!") DO (
            IF %%~zT GTR 0 (
                ECHO ----- ERROR IN FILE: "!FULLPATH!" -----\r\n >> "!LOG_FILE%"
                TYPE "!TEMP_ERR%" >> "!LOG_FILE%"
                ECHO \r\n----- END ERROR -----\r\n\r\n >> "!LOG_FILE%"
            )
        )
        
        REM --- CRITICAL FIX ---
        REM Using Delayed Expansion (!FULLPATH!) prevents special chars like & or ( ) 
        REM from being interpreted as commands.
        >>"!PROGRESS_FILE!" ECHO !FULLPATH!
        
    ) ELSE (
        REM File found in log, skipping.
    )
)

REM Clean up the temp file
IF EXIST "!TEMP_ERR!" (
    DEL "!TEMP_ERR!"
)

ECHO.
ECHO Probe complete.
ECHO Check !LOG_FILE% for any errors.

PAUSE