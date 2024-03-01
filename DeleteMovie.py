import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Define the movie name to delete
movie_to_delete = "Lego Batman"

# Execute the SQL DELETE statement
c.execute("DELETE FROM movies WHERE movie_name=?", (movie_to_delete,))
conn.commit()

# Close the connection to the database
conn.close()
