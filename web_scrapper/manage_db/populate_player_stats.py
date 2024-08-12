import sqlite3

def populate_player_urls():
    try:
        # Connect to the database
        conn = sqlite3.connect("../player_stats.db")
        cursor = conn.cursor()

        # Open the player_urls.out file and read its contents
        with open("../player_urls/player_urls.out", "r") as f:
            player_urls = [line.strip() for line in f.readlines()]

        # Insert each player URL into the player_urls table
        for url in player_urls:
            cursor.execute("INSERT OR IGNORE INTO player_urls (player_url) VALUES (?)", (url,))

        # Commit the changes
        conn.commit()

        print("Player URLs populated successfully!")

    except sqlite3.Error as e:
        print(f"Error populating player URLs: {e}")

    except FileNotFoundError:
        print("Error: player_urls.out file not found")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Close the connection
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    populate_player_urls()