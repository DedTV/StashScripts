import sqlite3
import csv

# Configuration
DB_PATH = r'E:\stash-go.sqlite'
OUTPUT_CSV = r'E:\MissingFolders.csv'

def find_missing_studio_folders():
    try:
        # Connect to the Stash database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQL Query: Find studios where there is no matching ID in the folders table
        # We use a LEFT JOIN and look for NULLs on the right side
        query = """
        SELECT s.id, s.name
        FROM studios s
        LEFT JOIN folders f ON s.id = f.id
        WHERE f.id IS NULL;
        """

        print(f"Scanning {DB_PATH} for missing folders...")
        cursor.execute(query)
        missing_studios = cursor.fetchall()

        if not missing_studios:
            print("Success! Every studio has a corresponding folder entry.")
            return

        # Write the results to CSV
        with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(['Studio ID', 'Studio Name'])
            # Data
            writer.writerows(missing_studios)

        print(f"Done! Found {len(missing_studios)} studios without folders.")
        print(f"List saved to: {OUTPUT_CSV}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    find_missing_studio_folders()