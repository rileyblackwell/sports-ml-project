import sqlite3

def populate_player_stats():
    # Connect to the database
    conn = sqlite3.connect("../player_stats.db")
    cursor = conn.cursor()

    # Open the player_urls.out file and read its contents
    with open("../player_urls/player_urls.out", "r") as f:
        player_urls = [line.strip() for line in f.readlines()]

    # Insert each player URL into the player_stats table
    for url in player_urls:
        cursor.execute("INSERT OR IGNORE INTO player_stats (player_url) VALUES (?)", (url,))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    print("Player stats populated successfully!")

if __name__ == '__main__':
    populate_player_stats()