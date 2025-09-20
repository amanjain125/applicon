import requests
import json

def test_api_endpoints():
    print("=== Testing API Endpoints ===")
    
    # Test statistics endpoint
    try:
        response = requests.get('http://localhost:5000/api/statistics')
        if response.status_code == 200:
            stats = response.json()
            print(f"Statistics endpoint working: {stats}")
        else:
            print(f"Statistics endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"Error testing statistics endpoint: {e}")
    
    # Test job titles endpoint
    try:
        response = requests.get('http://localhost:5000/api/job-titles')
        if response.status_code == 200:
            job_titles = response.json()
            print(f"Job titles endpoint working: {job_titles}")
        else:
            print(f"Job titles endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"Error testing job titles endpoint: {e}")

if __name__ == "__main__":
    test_api_endpoints()