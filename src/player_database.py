import sqlite3
import os

class PlayerDatabase:
    def __init__(self, db_path='players.db'):
        # Ensure the database path is absolute
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.path.dirname(__file__), db_path)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create the necessary tables if they don't exist"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            score INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            score INTEGER,
            date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
        ''')
        self.conn.commit()
    
    def add_player(self, username):
        """Add a new player to the database"""
        try:
            self.cursor.execute('INSERT INTO players (username) VALUES (?)', (username,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Player with this username already exists
            return False
    
    def get_player(self, username):
        """Get player details by username"""
        self.cursor.execute('SELECT * FROM players WHERE username = ?', (username,))
        return self.cursor.fetchone()
    
    def update_score(self, username, new_score):
        """Update a player's score and increment games_played"""
        player = self.get_player(username)
        if not player:
            return False
            
        player_id = player[0]
        
        # Update the player's total score and games played
        self.cursor.execute('''
        UPDATE players 
        SET score = score + ?, games_played = games_played + 1 
        WHERE id = ?
        ''', (new_score, player_id))
        
        # Record the game session
        self.cursor.execute('''
        INSERT INTO game_sessions (player_id, score) 
        VALUES (?, ?)
        ''', (player_id, new_score))
        
        self.conn.commit()
        return True
    
    def get_leaderboard(self, limit=10):
        """Get top players by score"""
        self.cursor.execute('''
        SELECT username, score, games_played 
        FROM players 
        ORDER BY score DESC 
        LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def get_player_history(self, username):
        """Get game history for a player"""
        player = self.get_player(username)
        if not player:
            return []
            
        player_id = player[0]
        self.cursor.execute('''
        SELECT score, date_played 
        FROM game_sessions 
        WHERE player_id = ? 
        ORDER BY date_played DESC
        ''', (player_id,))
        return self.cursor.fetchall()
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
