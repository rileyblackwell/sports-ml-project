import sqlite3

# Establish a connection to the database
conn = sqlite3.connect("player_data.db")
cursor = conn.cursor()

def create_player_outut_files(player_url):
    # Query the database to retrieve skill scores, weekly data, rookie seasons, and team ID
    cursor.execute("SELECT * FROM skill_scores WHERE player_url = ?", (player_url,))
    skill_scores = cursor.fetchone()
    
    cursor.execute("SELECT * FROM weekly_data WHERE player_url = ?", (player_url,))
    weekly_data = cursor.fetchone()
    
    cursor.execute("SELECT * FROM rookie_seasons WHERE player_url = ?", (player_url,))
    rookie_seasons = cursor.fetchone()
    
    cursor.execute("SELECT * FROM team_id WHERE player_url = ?", (player_url,))
    team_id = cursor.fetchone()
    
    # Process the data and return the results
    return skill_scores, weekly_data, rookie_seasons, team_id

def validate_player_data(player_url):
    # Query the database to retrieve the player data
    cursor.execute("SELECT * FROM player_data WHERE player_url = ?", (player_url,))
    player_data = cursor.fetchone()
    
    # Validate the data and return the result
    if player_data:
        # Data is valid, return True
        return True
    else:
        # Data is invalid, return False
        return False

def main():
    # Query the database to retrieve all player URLs
    cursor.execute("SELECT player_url FROM player_urls")
    player_urls = cursor.fetchall()
    
    for player_url in player_urls:
        # Create an output file containing only a single player URL
        # (Note: this might not be necessary with a database)
        
        # Call create_player_outut_files() and validate_player_data()
        skill_scores, weekly_data, rookie_seasons, team_id = create_player_outut_files(player_url)
        is_valid = validate_player_data(player_url)
        
        # Process the results and store them in the database
        if is_valid:
            # Store the valid data in the database
            cursor.execute("INSERT INTO valid_player_data VALUES (?, ?, ?, ?)", (player_url, skill_scores, weekly_data, rookie_seasons))
        else:
            # Store the invalid data in the database
            cursor.execute("INSERT INTO invalid_player_data VALUES (?, ?, ?, ?)", (player_url, skill_scores, weekly_data, rookie_seasons))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()