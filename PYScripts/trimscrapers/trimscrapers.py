import os
import sys

def find_folders_without_tlds(tld_file_path, search_root, output_file_path):
    """
    Outputs subdirectories where NONE of the contained files contain any TLDs.
    """
    # 1. Load the TLD list
    try:
        with open(tld_file_path, 'r', encoding='utf-8') as f:
            tlds = [line.strip().lower() for line in f if line.strip()]
        if not tlds:
            print("The TLD list is empty.")
            return
    except FileNotFoundError:
        print(f"Error: Could not find TLD file at {tld_file_path}")
        return

    folders_matched = 0
    total_folders_scanned = 0

    try:
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            print(f"Scanning root: {search_root}\n")

            # os.walk generates (current_path, subdirs, files) for every directory
            for root, dirs, files in os.walk(search_root):
                if not files:
                    continue  # Skip empty directories
                
                total_folders_scanned += 1
                folder_has_tld = False
                
                # Update progress
                sys.stdout.write(f"\r[Folders Scanned: {total_folders_scanned}] Checking: {root[-50:]}...   ")
                sys.stdout.flush()

                # 2. Check every file in the current directory
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            
                            # If ANY file contains ANY TLD, the whole folder is disqualified
                            if any(tld in content for tld in tlds):
                                folder_has_tld = True
                                break # Stop checking files in this folder
                                
                    except Exception:
                        # Silently skip files that can't be read to keep the UI clean
                        continue

                # 3. If the loop finished without finding a TLD, record the folder
                if not folder_has_tld:
                    out_file.write(root + "\n")
                    folders_matched += 1

    except PermissionError:
        print(f"\nError: Could not write to {output_file_path}.")
        return

    # Final Summary
    print("\n" + "-"*30)
    print("Search Complete.")
    print(f"Total folders evaluated: {total_folders_scanned}")
    print(f"Folders with zero TLD matches: {folders_matched}")
    print(f"Results saved to: {output_file_path}")

if __name__ == "__main__":
    TLD_INPUT = r"E:\TLDs.txt"
    SEARCH_ROOT = r"E:\scrapers\community"
    RESULT_OUTPUT = r"E:\results.txt"

    find_folders_without_tlds(TLD_INPUT, SEARCH_ROOT, RESULT_OUTPUT)