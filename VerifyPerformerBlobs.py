import os
import sqlite3

# Connect to the database
conn = sqlite3.connect('E:\\stash-go.sqlite')
c = conn.cursor()

# Query to get all checksums
c.execute("SELECT image_blob FROM performers")
rows = c.fetchall()

for row in rows:
    checksum = row[0]
    if checksum is not None:
        # Construct the file path
        file_path = f"K:\\StashData\\BinaryData\\{checksum[:2]}\\{checksum[2:4]}\\{checksum}"
        
        # Check if the file exists
        if not os.path.exists(file_path):
            # If the file does not exist, set the corresponding image_blob value to NULL
            c.execute("UPDATE performers SET image_blob = NULL WHERE image_blob = ?", (checksum,))
            
            # Commit the changes to the database
            conn.commit()
            
            print(f"Updated performers.image_blob for checksum {checksum} to NULL")
        else:
            print(f"File {file_path} exists. No action taken.")

# Close the connection
conn.close()
