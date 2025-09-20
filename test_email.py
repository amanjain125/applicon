import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email():
    # Email configuration
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email or not sender_password:
        print("Error: Email configuration not found in .env file")
        print("Make sure SENDER_EMAIL and SENDER_PASSWORD are set")
        return False
    
    # Test recipient (use your own email to test)
    recipient_email = input("Enter your email address to test: ")
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Test Email from Resume Evaluator"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Create text content
        text = """\
        This is a test email from the Resume Evaluator system.
        
        If you received this email, your email configuration is working correctly!
        """
        
        # Add text part
        part = MIMEText(text, "plain")
        message.attach(part)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print(f"Test email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send test email: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Email Configuration...")
    test_email()