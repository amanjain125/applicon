import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from parser.resume_parser import ResumeParser
from parser.jd_parser import JdParser

def test_parsers():
    print("=== Testing Parsers ===")
    
    # Test resume parser with job title extraction
    resume_parser = ResumeParser()
    
    # Sample resume text
    sample_resume = """John Doe
Senior Data Scientist

Email: john.doe@example.com
Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe

SUMMARY
Experienced data scientist with 5 years of experience in machine learning and Python.

EXPERIENCE
Senior Data Scientist | Tech Solutions Inc. | Jan 2020 - Present
- Developed machine learning models using Python and TensorFlow
- Led a team of 3 data analysts

Data Analyst | Innovate Co. | Jun 2017 - Dec 2019
- Analyzed large datasets using Python and pandas
- Created dashboards with Power BI
"""
    
    print("Testing resume parser...")
    try:
        resume_data = resume_parser.parse_from_text(sample_resume)
        print(f"Extracted job title: {resume_data.get('job_title', 'Not found')}")
        print(f"Extracted email: {resume_data.get('email', 'Not found')}")
    except Exception as e:
        print(f"Error testing resume parser: {e}")
    
    # Test JD parser
    jd_parser = JdParser()
    
    # Sample JD text
    sample_jd = """Senior Data Scientist Position

We are looking for an experienced Senior Data Scientist with expertise in machine learning.

Requirements:
- 5+ years of experience with Python
- Experience with TensorFlow and machine learning frameworks
- Knowledge of data visualization tools

Nice to have:
- Team leadership experience
- Experience with cloud platforms
"""
    
    print("\nTesting JD parser...")
    jd_data = jd_parser.parse(sample_jd)
    print(f"Extracted job title: {jd_data.get('job_title', 'Not found')}")
    print(f"Must-have skills: {jd_data.get('must_have_skills', [])}")
    print(f"Good-to-have skills: {jd_data.get('good_to_have_skills', [])}")

if __name__ == "__main__":
    test_parsers()