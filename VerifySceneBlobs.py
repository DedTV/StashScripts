import sqlite3
import os

# Connect to the database
conn = sqlite3.connect('E:\\stash-go.sqlite')
c = conn.cursor()

# Query to get all checksums
c.execute("SELECT checksum FROM blobs")
rows = c.fetchall()

for row in rows:
    checksum = row[0]
    # Construct the file path
    file_path = f"K:\\StashData\\BinaryData\\{checksum[:2]}\\{checksum[2:4]}\\{checksum}"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Deleting row with checksum {checksum}...")
        
        # Delete the row with the invalid checksum
        c.execute("DELETE FROM blobs WHERE checksum = ?", (checksum,))
               
        # Commit the database changes
        conn.commit()
        
        print(f"Row with checksum {checksum} deleted.")
    else:
        print(f"File {file_path} exists. No action taken.")

# Close the connection to the database
conn.close()
