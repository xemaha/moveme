import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Execute SQL command to delete all records from the movies table
c.execute("DELETE FROM movies")

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("All entries deleted from the database.")