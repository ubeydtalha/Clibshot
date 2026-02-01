"""
Database session management.
"""

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator


# Database path
DB_PATH = Path.home() / ".clipshot" / "clipshot.db"


class DatabaseSession:
    """Simple async database session wrapper."""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        """Enter context manager."""
        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


@asynccontextmanager
async def get_session() -> AsyncGenerator[sqlite3.Cursor, None]:
    """Get an async database session."""
    with DatabaseSession() as cursor:
        yield cursor
