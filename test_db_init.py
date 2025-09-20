import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from models.database import EvaluationDatabase

def test_database_init():
    print("=== Testing Database Initialization ===")
    
    try:
        db = EvaluationDatabase()
        print("Database initialized successfully")
        
        # Check schema again
        import sqlite3
        conn = sqlite3.connect("evaluations.db")
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(evaluations)")
        columns = cursor.fetchall()
        
        print("Updated table schema:")
        for column in columns:
            print(f"  {column[1]} ({column[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_init()