import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.email_service import EmailService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_service():
    print("Testing Email Service...")
    
    # Initialize email service
    email_service = EmailService()
    
    # Check if configured
    if not email_service.is_configured():
        print("Email service is not properly configured!")
        print("Please check your .env file and make sure SENDER_EMAIL and SENDER_PASSWORD are set.")
        return
    
    # Test email data
    test_evaluation = {
        "email": "test@example.com",
        "job_title": "Data Analyst Position",
        "relevance_score": 75.5,
        "verdict": "Medium",
        "feedback": "Your resume shows good potential but is missing some key requirements.",
        "missing_elements": {
            "must_have_skills": ["Python", "SQL"],
            "good_to_have_skills": ["Tableau", "Machine Learning"],
            "qualifications": ["Bachelor's Degree in Data Science"]
        }
    }
    
    print("\nTesting single email sending...")
    success = email_service.send_feedback_email(test_evaluation)
    
    if success:
        print("✓ Email sent successfully!")
    else:
        print("✗ Failed to send email")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    test_email_service()