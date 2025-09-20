import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import ResumeEvaluator

def test_single_evaluation():
    print("=== Testing Single Evaluation ===")
    
    # Create sample files for testing
    print("Creating sample files...")
    
    # Sample resume
    resume_content = """John Doe
Data Scientist

Email: john.doe@example.com
Phone: (555) 123-4567

SUMMARY
Experienced data scientist with 3 years of experience in Python and machine learning.

EXPERIENCE
Data Scientist | Tech Solutions Inc. | jan2020 - Present
- Developed machine learning models using Python and TensorFlow
- Created dashboards with Power BI
"""
    
    # Sample JD
    jd_content = """Data Scientist Position

We are looking for a Data Scientist with experience in Python and machine learning.

Requirements:
- 2+ years of experience with Python
- Experience with machine learning frameworks
- Knowledge of data visualization tools

Nice to have:
- Experience with Power BI
- Cloud platform experience
"""
    
    # Write sample files
    with open("test_resume.txt", "w") as f:
        f.write(resume_content)
    
    with open("test_jd.txt", "w") as f:
        f.write(jd_content)
    
    try:
        evaluator = ResumeEvaluator()
        print("Evaluator initialized.")
        
        # Test the resume parser directly first
        from parser.resume_parser import ResumeParser
        resume_parser = ResumeParser()
        resume_data = resume_parser.parse_from_text(resume_content)
        print(f"Resume parsed - Email: {resume_data.get('email')}, Phone: {resume_data.get('phone')}, Job Title: {resume_data.get('job_title')}")
        
        # Test the JD parser directly
        from parser.jd_parser import JdParser
        jd_parser = JdParser()
        jd_data = jd_parser.parse(jd_content)
        print(f"JD parsed - Job Title: {jd_data.get('job_title')}")
        
        print("Testing evaluation...")
        result = evaluator.evaluate("test_resume.txt", "test_jd.txt")
        print("Evaluation successful!")
        print(f"Score: {result['relevance_score']}")
        print(f"Verdict: {result['verdict']}")
        print(f"Email: {result['email']}")
        print(f"Phone: {result['phone']}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    try:
        os.remove("test_resume.txt")
        os.remove("test_jd.txt")
    except:
        pass

if __name__ == "__main__":
    test_single_evaluation()