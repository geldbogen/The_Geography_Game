from player_database import PlayerDatabase

def main():
    # Create a database instance
    db = PlayerDatabase()
    
    # Example operations
    
    # Add players
    db.add_player("Player1")
    db.add_player("Player2")
    
    # Update scores
    db.update_score("Player1", 120)
    db.update_score("Player2", 85)
    db.update_score("Player1", 150)
    
    # Get a specific player
    player = db.get_player("Player1")
    if player:
        print(f"Player: {player[1]}, Score: {player[2]}, Games: {player[3]}")
    
    # Display leaderboard
    print("\nLeaderboard:")
    for rank, (username, score, games) in enumerate(db.get_leaderboard(), 1):
        print(f"{rank}. {username}: {score} points ({games} games)")
    
    # Show player history
    print("\nPlayer1 History:")
    for score, date in db.get_player_history("Player1"):
        print(f"Score: {score}, Date: {date}")
    
    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()
