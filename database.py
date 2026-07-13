import sqlite3

# Connect to database (creates it if it doesn't exist)
connection = sqlite3.connect("clinic.db")

# Create a cursor
cursor = connection.cursor()

# Create appointments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    date TEXT,
    treatment TEXT,
    message TEXT
)
""")

# Save changes
connection.commit()

# Close connection
connection.close()

print("Database created successfully!")