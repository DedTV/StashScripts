import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import multiprocessing

# --- CONFIGURATION ---
# IMPORTANT: Adjust ROOT_DIR to your actual starting directory
ROOT_DIR = r"F:\Stashed" 
LOG_FILE = "error.log"               # Detailed error descriptions
BAD_FILES_LOG = "bad_files.txt"      # Simple list of paths for bad files (Only for files with actual FFmpeg errors)
PROGRESS_FILE = "processed_files.log" # History of scanned files (Successful files and those with FFmpeg errors)
EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv"} 

# Set the number of worker processes (a good starting point is the number of CPU cores)
MAX_WORKERS = 4 
TIMEOUT_SECONDS = 600 # Time in seconds before the probe times out

# --- UTILITY FUNCTIONS (Process-Safe) ---

def load_processed_files(filepath):
    """Loads already processed file paths into a set for O(1) lookup."""
    processed = set()
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    processed.add(line.strip())
        except Exception as e:
            print(f"Warning: Could not read progress file: {e}", file=sys.stderr)
    return processed

def append_to_file(filepath, text):
    """Appends a line to a file safely. Using 'a' mode handles concurrent writes 
       at the OS level reasonably well for simple text lines."""
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception as e:
        print(f"Error writing to {filepath}: {e}", file=sys.stderr)

def log_detailed_error(log_path, video_path, error_message):
    """Logs detailed ffmpeg errors to the main error log."""
    header = f"----- ERROR IN FILE: {video_path} -----\n"
    footer = f"\n----- END ERROR -----\n\n"
    
    append_to_file(log_path, header + error_message + footer.strip())


# --- WORKER FUNCTION ---

def probe_video_worker(full_path, log_path, bad_files_path):
    """
    Function executed by each worker process to check a single video file.
    Returns: A tuple (full_path, status)
    status: True (Success), False (FFmpeg Error), "TIMEOUT" (Timeout), "FFMPEG_MISSING" (Critical Error)
    """
    filename = os.path.basename(full_path)
    
    try:
        # Run FFmpeg
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", full_path, "-f", "null", "-"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS # Use the configured timeout
        )

        # Handle Errors
        if result.stderr:
            # An actual FFmpeg error occurred. Log it.
            log_detailed_error(log_path, full_path, result.stderr)
            append_to_file(bad_files_path, full_path)
            return (full_path, False) 
        
        # No error detected.
        return (full_path, True) 

    except FileNotFoundError:
        return (full_path, "FFMPEG_MISSING") 
    
    except subprocess.TimeoutExpired:
        # File skipped for re-processing later
        return (full_path, "TIMEOUT")
        
    except Exception as e:
        # Treat unexpected errors as failures that should be logged as processed
        return (full_path, False)


# --- MAIN EXECUTION (Modified) ---

def main():
    # 1. Setup and Initialization
    print(f"--- Starting Video Probe (Multiprocessing) ---")
    print(f"Root: {ROOT_DIR}")
    print(f"Workers: {MAX_WORKERS} | Timeout: {TIMEOUT_SECONDS}s")
    
    # Clear old logs ONLY if starting fresh
    if not os.path.exists(PROGRESS_FILE):
        print("Fresh start detected. Clearing old logs.")
        if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
        if os.path.exists(BAD_FILES_LOG): os.remove(BAD_FILES_LOG)
    else:
        print("Resuming from previous scan...")

    processed_files = load_processed_files(PROGRESS_FILE)
    print(f"Found {len(processed_files)} files already scanned.")

    # 2. Collect files to scan
    files_to_scan = []
    for root, dirs, files in os.walk(ROOT_DIR):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext.lower() in EXTENSIONS:
                full_path = os.path.join(root, filename)
                if full_path not in processed_files:
                    files_to_scan.append(full_path)

    total_new_files = len(files_to_scan)
    if total_new_files == 0:
        print("No new files found to scan. Exiting.")
        return

    print(f"Found {total_new_files} new files to scan. Starting parallel processing...")
    
    # 3. Parallel Execution
    start_time = time.time()
    files_processed_count = 0

    try:
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all files to the pool
            futures = {
                executor.submit(
                    probe_video_worker, 
                    f, 
                    LOG_FILE, 
                    BAD_FILES_LOG
                ): f
                for f in files_to_scan
            }
            
            # Use as_completed to process results as they finish (non-blocking)
            for future in as_completed(futures):
                files_processed_count += 1
                current_file_path = futures[future]
                filename = os.path.basename(current_file_path)
                
                try:
                    full_path, status = future.result()
                    
                    # --- ADDED CODE: Print completion status to console ---
                    status_message = ""
                    if status is True:
                        status_message = "OK"
                        append_to_file(PROGRESS_FILE, full_path)
                    elif status is False:
                        status_message = "ERROR (Logged)"
                        append_to_file(PROGRESS_FILE, full_path)
                    elif status == "TIMEOUT":
                        status_message = "TIMEOUT (Skipped for re-run)"
                        # Do NOT log to PROGRESS_FILE
                    elif status == "FFMPEG_MISSING":
                        print("CRITICAL: 'ffmpeg' not found. Shutting down pool.")
                        executor.shutdown(wait=False, cancel_futures=True)
                        sys.exit(1)
                    
                    # Print the completion message for the file
                    print(f"[{files_processed_count}/{total_new_files}] FINISHED: {filename} - Status: {status_message}")
                    # --- END ADDED CODE ---

                except Exception as e:
                    print(f"Main process caught an exception from a worker on {current_file_path}: {e}", file=sys.stderr)
                    # For safety, log the file as processed to avoid re-running if an unexpected error occurred.
                    append_to_file(PROGRESS_FILE, current_file_path) 


    except KeyboardInterrupt:
        print("\nScan interrupted by user (Ctrl+C). Shutting down.")
        sys.exit(0)

    end_time = time.time()
    
    # 4. Final Summary
    print("\n--- Probe Complete ---")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    print(f"Files checked:    {files_processed_count}")
    print(f"Detailed errors:  {LOG_FILE}")
    print(f"Bad file list:    {BAD_FILES_LOG} (Only actual FFmpeg errors)")

if __name__ == "__main__":
    multiprocessing.freeze_support() 
    main()