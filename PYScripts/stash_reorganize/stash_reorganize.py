import sqlite3
import os

DB_PATH = r"E:\stash-go.sqlite"

def restore():
    print("--- Phase 2: Restore Organized Status ---")
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if tracker exists and has data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tmp_organized_tracker'")
        if not cursor.fetchone():
            print("ABORT: No tracker table found. Nothing to restore.")
            return

        cursor.execute("SELECT count() FROM tmp_organized_tracker")
        count = cursor.fetchone()[0]
        if count == 0:
            print("ABORT: Tracker is empty. Nothing to restore.")
            return

        print(f"Attempting to restore {count} scenes...")
        
        # SMART RESTORE: Only update if the scene is still 0
        cursor.execute("""
            UPDATE scenes 
            SET organized = 1 
            WHERE organized = 0 
            AND id IN (SELECT scene_id FROM tmp_organized_tracker)
        """)
        affected = cursor.rowcount
        
        # Clean up
        cursor.execute("DROP TABLE tmp_organized_tracker")
        conn.commit()
        
        print(f"SUCCESS: {affected} scenes restored to Organized.")
        if affected < count:
            print(f"Note: {count - affected} scenes were already marked Organized by Stash and were left alone.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    restore()