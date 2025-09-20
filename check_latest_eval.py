import sqlite3

def check_latest_evaluation():
    print("=== Checking Latest Evaluation ===")
    
    conn = sqlite3.connect("evaluations.db")
    cursor = conn.cursor()
    
    # Get the latest evaluation
    cursor.execute("SELECT * FROM evaluations ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        print("Latest evaluation:")
        columns = [description[0] for description in cursor.description]
        for i, (col, val) in enumerate(zip(columns, row)):
            print(f"  {col}: {val}")
    else:
        print("No evaluations found")
    
    conn.close()

if __name__ == "__main__":
    check_latest_evaluation()