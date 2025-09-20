import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import os
from jinja2 import Template

class EmailService:
    """Service for sending emails to candidates with their evaluation results"""
    
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.sender_name = os.getenv('SENDER_NAME', 'Applicon Resume Evaluator')
        
        # Print debug information
        print(f"Email Service Configuration:")
        print(f"  SMTP Server: {self.smtp_server}")
        print(f"  SMTP Port: {self.smtp_port}")
        print(f"  Sender Email: {'*' * len(self.sender_email) if self.sender_email else 'NOT SET'}")
        print(f"  Sender Password: {'SET' if self.sender_password else 'NOT SET'}")
        print(f"  Sender Name: {self.sender_name}")
    
    def send_feedback_email(self, evaluation_result: Dict) -> bool:
        """Send feedback email to candidate"""
        # Check if we have email address
        candidate_email = evaluation_result.get('email', '')
        print(f"Attempting to send email to: {candidate_email}")
        
        if not candidate_email:
            print("No email address found for candidate")
            return False
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, candidate_email):
            print(f"Invalid email format: {candidate_email}")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Resume Evaluation Feedback - {evaluation_result.get('job_title', 'Position')}"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = candidate_email
            
            print(f"Email details:")
            print(f"  Subject: {message['Subject']}")
            print(f"  From: {message['From']}")
            print(f"  To: {message['To']}")
            
            # Create HTML content
            html_content = self._generate_email_html(evaluation_result)
            
            # Add HTML part to message
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create plain text content as fallback
            text_content = self._generate_email_text(evaluation_result)
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)
            
            # Send email
            print("Connecting to SMTP server...")
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                print("Starting TLS...")
                server.starttls(context=context)
                print("Logging in...")
                server.login(self.sender_email, self.sender_password)
                print("Sending email...")
                server.sendmail(self.sender_email, candidate_email, message.as_string())
            
            print(f"Feedback email sent successfully to {candidate_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email to {candidate_email}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def send_batch_feedback_emails(self, evaluation_results: List[Dict]) -> Dict:
        """Send feedback emails to multiple candidates"""
        print(f"Sending batch emails to {len(evaluation_results)} candidates")
        success_count = 0
        failure_count = 0
        failed_emails = []
        
        for i, result in enumerate(evaluation_results):
            print(f"Processing candidate {i+1}/{len(evaluation_results)}")
            if self.send_feedback_email(result):
                success_count += 1
            else:
                failure_count += 1
                if result.get('email'):
                    failed_emails.append(result['email'])
        
        print(f"Batch email sending complete: {success_count} successful, {failure_count} failed")
        return {
            "success_count": success_count,
            "failure_count": failure_count,
            "failed_emails": failed_emails
        }
    
    def _generate_email_html(self, evaluation_result: Dict) -> str:
        """Generate HTML email content"""
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #4a6fa5; color: white; padding: 20px; text-align: center; }
                .score-box { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin: 20px 0; }
                .high { background-color: #d4edda; border-color: #c3e6cb; }
                .medium { background-color: #fff3cd; border-color: #ffeaa7; }
                .low { background-color: #f8d7da; border-color: #f5c6cb; }
                .section { margin: 15px 0; }
                .footer { text-align: center; margin-top: 30px; font-size: 0.9em; color: #6c757d; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Resume Evaluation Feedback</h1>
                    <p>{{ job_title }}</p>
                </div>
                
                <p>Dear Candidate,</p>
                
                <p>Thank you for your interest in the <strong>{{ job_title }}</strong> position. We've evaluated your resume and would like to provide you with feedback to help improve your chances in future applications.</p>
                
                <div class="score-box {{ verdict.lower() }}">
                    <h2>Relevance Score: {{ relevance_score }}/100</h2>
                    <p><strong>Verdict: {{ verdict }}</strong></p>
                </div>
                
                <div class="section">
                    <h3>Feedback</h3>
                    <p>{{ feedback }}</p>
                </div>
                
                {% if missing_elements.must_have_skills or missing_elements.good_to_have_skills or missing_elements.qualifications %}
                <div class="section">
                    <h3>Missing Elements</h3>
                    {% if missing_elements.must_have_skills %}
                    <p><strong>Required Skills:</strong> {{ missing_elements.must_have_skills|join(', ') }}</p>
                    {% endif %}
                    {% if missing_elements.good_to_have_skills %}
                    <p><strong>Preferred Skills:</strong> {{ missing_elements.good_to_have_skills|join(', ') }}</p>
                    {% endif %}
                    {% if missing_elements.qualifications %}
                    <p><strong>Qualifications:</strong> {{ missing_elements.qualifications|join(', ') }}</p>
                    {% endif %}
                </div>
                {% endif %}
                
                <div class="section">
                    <h3>Next Steps</h3>
                    <p>
                        {% if verdict == 'High' %}
                        Your profile is a strong match for this position. We recommend applying directly through our careers page.
                        {% elif verdict == 'Medium' %}
                        Consider addressing the missing elements mentioned above to improve your profile for similar positions.
                        {% else %}
                        We recommend working on the areas highlighted above before applying for similar positions.
                        {% endif %}
                    </p>
                </div>
                
                <div class="footer">
                    <p>This feedback is provided by Innomatics Research Labs to help you improve your career prospects.</p>
                    <p>Please do not reply to this email as it is sent from an automated system.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Render template with evaluation data
        jinja_template = Template(template)
        return jinja_template.render(**evaluation_result)
    
    def _generate_email_text(self, evaluation_result: Dict) -> str:
        """Generate plain text email content"""
        text = f"""
Resume Evaluation Feedback - {evaluation_result.get('job_title', 'Position')}

Dear Candidate,

Thank you for your interest in the {evaluation_result.get('job_title', 'position')}. We've evaluated your resume and would like to provide you with feedback to help improve your chances in future applications.

Relevance Score: {evaluation_result.get('relevance_score', 'N/A')}/100
Verdict: {evaluation_result.get('verdict', 'N/A')}

Feedback:
{evaluation_result.get('feedback', 'No feedback available')}

"""
        
        missing_elements = evaluation_result.get('missing_elements', {})
        if missing_elements:
            text += "Missing Elements:\n"
            if missing_elements.get('must_have_skills'):
                text += f"Required Skills: {', '.join(missing_elements['must_have_skills'])}\n"
            if missing_elements.get('good_to_have_skills'):
                text += f"Preferred Skills: {', '.join(missing_elements['good_to_have_skills'])}\n"
            if missing_elements.get('qualifications'):
                text += f"Qualifications: {', '.join(missing_elements['qualifications'])}\n"
        
        text += f"""
Next Steps:
"""
        
        verdict = evaluation_result.get('verdict', '')
        if verdict == 'High':
            text += "Your profile is a strong match for this position. We recommend applying directly through our careers page."
        elif verdict == 'Medium':
            text += "Consider addressing the missing elements mentioned above to improve your profile for similar positions."
        else:
            text += "We recommend working on the areas highlighted above before applying for similar positions."
        
        text += """
        
This feedback is provided by Innomatics Research Labs to help you improve your career prospects.
Please do not reply to this email as it is sent from an automated system.
"""
        
        return text
    
    def is_configured(self) -> bool:
        """Check if email service is properly configured"""
        configured = bool(self.sender_email and self.sender_password)
        print(f"Email service configured: {configured}")
        if not configured:
            print("Email service not configured - missing sender email or password")
        return configured