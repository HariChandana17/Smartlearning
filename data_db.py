import sqlite3

# Connect to the database (replace 'your_database.db' with your database file)
connection = sqlite3.connect('learning_hub.db')

# Create a cursor object
cursor = connection.cursor()

# Write an SQL query (modify 'table_name' to your table name)
query = "SELECT username FROM users"

# Execute the query
cursor.execute(query)

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Display each row
for row in rows:
    print(row)

# Close the connection
connection.close()
