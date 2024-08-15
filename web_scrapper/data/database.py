import sqlite3

def read_player_data_from_db():
    """Reads player data from the database and returns it as a list of rows."""
    try:
        conn = sqlite3.connect("web_scrapper/player_stats.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player_weekly_data")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Error reading from database: {e}")
        return []