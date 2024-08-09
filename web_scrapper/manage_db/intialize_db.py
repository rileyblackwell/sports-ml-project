import sqlite3
import os

def create_database():
    # Define the database path
    db_path = os.path.join("..", "player_stats.db")

    # Connect to the database (create if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the "player_stats" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            player_url TEXT PRIMARY KEY UNIQUE,
            webpage TEXT
        )
    ''')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print("Database created successfully!")

if __name__ == '__main__':
    create_database()