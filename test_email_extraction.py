import re

def test_email_extraction():
    # Example resume text (you can replace this with actual resume content)
    sample_resume = """
    John Doe
    Data Analyst
    
    Email: john.doe@example.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    
    SUMMARY
    Experienced data analyst with 3 years of experience in Python and SQL.
    
    EXPERIENCE
    Data Analyst | Tech Solutions Inc. | jan2020 - Present
    - Analyzed large datasets using Python and pandas
    - Created dashboards with Power BI
    - Contact: j.doe@techsolutions.com
    """
    
    # Email extraction pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, sample_resume)
    
    print("Sample Resume Text:")
    print(sample_resume)
    print("\nExtracted Emails:")
    if emails:
        for email in emails:
            print(f"  - {email}")
    else:
        print("  No emails found")
    
    # Test with your actual resume
    print("\n" + "="*50)
    print("Test with your resume:")
    resume_path = input("Enter path to a resume file (or press Enter to skip): ")
    
    if resume_path:
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            text = None
            
            for encoding in encodings:
                try:
                    with open(resume_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if text:
                emails = re.findall(email_pattern, text)
                print(f"\nExtracted emails from {resume_path}:")
                if emails:
                    for email in emails:
                        print(f"  - {email}")
                else:
                    print("  No emails found")
            else:
                print("Could not read the file with any encoding")
                
        except Exception as e:
            print(f"Error reading file: {e}")

if __name__ == "__main__":
    test_email_extraction()