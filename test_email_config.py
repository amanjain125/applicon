import os
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

def test_email_config():
    print("=== Testing Email Configuration ===")
    
    # Check environment variables
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    sender_name = os.getenv('SENDER_NAME', 'Resume Evaluator')
    
    print(f"SMTP Server: {smtp_server or 'NOT SET'}")
    print(f"SMTP Port: {smtp_port or 'NOT SET'}")
    print(f"Sender Email: {sender_email or 'NOT SET'}")
    print(f"Sender Password: {'SET' if sender_password else 'NOT SET'}")
    print(f"Sender Name: {sender_name}")
    
    # Check if all required variables are set
    if not smtp_server or not smtp_port or not sender_email or not sender_password:
        print("\nERROR: Missing required email configuration!")
        print("Please update your .env file with the correct values.")
        return False
    
    print("\nSUCCESS: All email configuration variables are set!")
    return True

if __name__ == "__main__":
    test_email_config()