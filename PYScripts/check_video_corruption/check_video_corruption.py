import os
import subprocess
import csv
import logging
import concurrent.futures
import json

def check_video_corruption(filepath, processed_files):
    """Checks a video file for corruption using ffmpeg."""
    if filepath in processed_files:
        print(f"Skipping already processed file: {filepath}")
        return None, None, None

    print(f"Checking file: {filepath}") #debug
    try:
        command = [
            'ffmpeg',
            '-hwaccel', 'cuda',
            '-hwaccel_output_format', 'cuda',
            '-v', 'error',
            '-i', filepath,
            '-f', 'null', '-'
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode != 0:
            if "error" in result.stderr.lower() or "decode" in result.stderr.lower():
                unreadable_frames = result.stderr.lower().count("decode")
                logging.error(f"Corruption detected in {filepath}: {result.stderr}")
                print(f"Corruption detected in {filepath}: {result.stderr}")#debug
                return filepath, unreadable_frames, result.stderr
            else:
                return None, None, None
        else:
            return None, None, None
    except Exception as e:
        logging.exception(f"Error processing {filepath}: {e}")
        print(f"Error processing {filepath}: {e}")#debug
        return filepath, None, str(e)

def scan_directory(directory, csv_filename, log_filename, processed_files_filename):
    """Scans a directory for video files and checks for corruption."""
    video_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.mp4')]
    corrupted_files = []

    try:
        with open(processed_files_filename, 'r') as f:
            processed_files = json.load(f)
    except FileNotFoundError:
        processed_files = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(check_video_corruption, filepath, processed_files) for filepath in video_files]
        for future in concurrent.futures.as_completed(futures):
            filepath, unreadable_frames, error_message = future.result()
            if filepath:
                corrupted_files.append((filepath, unreadable_frames))
            else:
                current_file = future.result()
                if current_file is not None:
                    if current_file[0] is not None:
                        if current_file[0] not in processed_files:
                            if current_file[0].lower().endswith(".mp4"):
                                processed_files.append(current_file[0])

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filepath', 'Unreadable Frames'])
        for filepath, unreadable_frames in corrupted_files:
            writer.writerow([filepath, unreadable_frames])

    with open(processed_files_filename, 'w') as f:
        json.dump(processed_files, f)

    print(f"Scan complete. Corrupted files written to {csv_filename}. Errors logged to {log_filename}")

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan: ")
    csv_filename = "corrupted_videos.csv"
    log_filename = "corrupted_videos.log"
    processed_files_filename = "processed_files.json"

    logging.basicConfig(filename=log_filename, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    scan_directory(directory_to_scan, csv_filename, log_filename, processed_files_filename)