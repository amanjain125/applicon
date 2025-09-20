import sqlite3
import json

def inspect_database():
    print("=== Inspecting Database ===")
    
    conn = sqlite3.connect("evaluations.db")
    cursor = conn.cursor()
    
    # Get all unique job titles
    cursor.execute("SELECT DISTINCT job_title FROM evaluations")
    rows = cursor.fetchall()
    
    print("All job titles in database:")
    for i, row in enumerate(rows):
        print(f"  {i+1}. {repr(row[0])}")
    
    # Get a few sample evaluations
    cursor.execute("SELECT id, job_title, resume_filename FROM evaluations LIMIT 5")
    sample_rows = cursor.fetchall()
    
    print("\nSample evaluations:")
    for row in sample_rows:
        print(f"  ID: {row[0]}, Job Title: {repr(row[1])}, Resume: {row[2]}")
    
    conn.close()

if __name__ == "__main__":
    inspect_database()