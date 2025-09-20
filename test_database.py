import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from models.database import EvaluationDatabase

def test_database():
    print("=== Testing Database ===")
    
    # Initialize database
    db = EvaluationDatabase()
    
    # Test statistics
    try:
        stats = db.get_statistics()
        print(f"Database statistics: {stats}")
    except Exception as e:
        print(f"Error getting statistics: {e}")
    
    # Test unique job titles
    try:
        job_titles = db.get_unique_job_titles()
        print(f"Unique job titles: {job_titles}")
    except Exception as e:
        print(f"Error getting job titles: {e}")

if __name__ == "__main__":
    test_database()