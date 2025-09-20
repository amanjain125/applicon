import os
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.email_service import EmailService

# Load environment variables
load_dotenv()

def test_email_sending():
    print("=== Testing Email Sending ===")
    
    # Initialize email service
    email_service = EmailService()
    
    # Check if configured
    if not email_service.is_configured():
        print("ERROR: Email service is not properly configured!")
        return
    
    # Test email data
    test_data = {
        "email": "amangattu5678@gmail.com",  # Use your own email for testing
        "job_title": "Data Analyst Position",
        "relevance_score": 85.5,
        "verdict": "High",
        "feedback": "Your resume shows excellent potential for this position. Your skills in Python and SQL match the requirements well.",
        "missing_elements": {
            "must_have_skills": [],
            "good_to_have_skills": ["Machine Learning", "Tableau"],
            "qualifications": []
        }
    }
    
    print(f"Sending test email to: {test_data['email']}")
    
    # Try to send email
    try:
        success = email_service.send_feedback_email(test_data)
        if success:
            print("SUCCESS: Email sent successfully!")
        else:
            print("ERROR: Failed to send email")
    except Exception as e:
        print(f"ERROR: Exception occurred while sending email: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email_sending()