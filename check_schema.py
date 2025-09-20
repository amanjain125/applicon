import sqlite3

def check_database_schema():
    print("=== Checking Database Schema ===")
    
    conn = sqlite3.connect("evaluations.db")
    cursor = conn.cursor()
    
    # Get table schema
    cursor.execute("PRAGMA table_info(evaluations)")
    columns = cursor.fetchall()
    
    print("Current table schema:")
    for column in columns:
        print(f"  {column[1]} ({column[2]})")
    
    conn.close()

if __name__ == "__main__":
    check_database_schema()