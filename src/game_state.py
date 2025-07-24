"""Shared game state module to avoid circular imports"""

from backend_game import BackendGame
from typing import Optional

# Global backend game instance
BACKEND_GAME: BackendGame = BackendGame()

def set_backend_game(backend_game: BackendGame) -> None:
    """Set the global backend game instance"""
    global BACKEND_GAME
    BACKEND_GAME = backend_game

def get_backend_game() -> BackendGame:
    """Get the global backend game instance"""
    global BACKEND_GAME
    return BACKEND_GAME

def reset_backend_game() -> None:
    """Reset the backend game instance"""
    global BACKEND_GAME
    BACKEND_GAME = BackendGame()

def is_backend_game_initialized() -> bool:
    """Check if backend game is initialized"""
    global BACKEND_GAME
    return BACKEND_GAME is not None