import sqlite3
import os
import sys

# Configuration
DB_PATH = r"E:\stash-go.sqlite"

def run_toggle():
    print("--- Stash Toggle Debug Start ---")
    
    # 1. Check if file exists
    if not os.path.exists(DB_PATH):
        print(f"CRITICAL: Database file NOT found at: {DB_PATH}")
        print("Please verify the drive letter and path.")
        return
    else:
        print(f"SUCCESS: Found database file at {DB_PATH}")

    try:
        print("Attempting to connect to the database...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("SUCCESS: Database connection established.")

        # 2. Check table existence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scenes'")
        if not cursor.fetchone():
            print("CRITICAL: The table 'scenes' does not exist in this database. Are you sure this is the Stash DB?")
            return
        
        # 3. Setup tracker table
        print("Ensuring 'tmp_organized_tracker' table exists...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tmp_organized_tracker (
                scene_id INTEGER PRIMARY KEY
            )
        """)
        conn.commit()

        # 4. Check current state
        cursor.execute("SELECT count() FROM tmp_organized_tracker")
        tracker_count = cursor.fetchone()[0]
        print(f"DEBUG: Current tracker table count: {tracker_count}")

        if tracker_count > 0:
            # --- REVERT MODE ---
            print("Action: REVERT MODE detected (tracker is not empty).")
            cursor.execute("""
                UPDATE scenes 
                SET organized = 1 
                WHERE id IN (SELECT scene_id FROM tmp_organized_tracker)
            """)
            affected = cursor.rowcount
            print(f"DEBUG: Updated {affected} rows in 'scenes' to organized=1.")
            
            cursor.execute("DELETE FROM tmp_organized_tracker")
            conn.commit()
            print("SUCCESS: Reverted scenes and cleared tracker.")

        else:
            # --- MODIFY MODE ---
            print("Action: MODIFY MODE detected (tracker is empty).")
            
            # Check how many are currently organized
            cursor.execute("SELECT count() FROM scenes WHERE organized = 1")
            org_count = cursor.fetchone()[0]
            print(f"DEBUG: Found {org_count} scenes currently set to 'Organized' (1).")

            if org_count == 0:
                print("ABORT: No scenes found with 'organized = 1'. Nothing to do.")
                return

            # Get IDs
            cursor.execute("SELECT id FROM scenes WHERE organized = 1")
            ids = [row[0] for row in cursor.fetchall()]

            # Insert into tracker
            print(f"Inserting {len(ids)} IDs into tracker...")
            cursor.executemany("INSERT INTO tmp_organized_tracker (scene_id) VALUES (?)", [(id,) for id in ids])
            
            # Set to 0
            print("Updating scenes to 'Unorganized' (0)...")
            cursor.execute("UPDATE scenes SET organized = 0 WHERE id IN (SELECT scene_id FROM tmp_organized_tracker)")
            
            conn.commit()
            print(f"SUCCESS: {len(ids)} scenes set to 0. Ready for Identify task.")

    except sqlite3.Error as e:
        print(f"SQLITE ERROR: {e}")
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")
    
    print("--- Debug End ---")

if __name__ == "__main__":
    run_toggle()