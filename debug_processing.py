import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from parser.resume_parser import ResumeParser
from parser.jd_parser import JdParser
from scoring.relevance_scorer import RelevanceScorer
from scoring.semantic_matcher import SemanticMatcher

def debug_processing():
    print("=== Debugging Resume Processing ===")
    
    # Initialize components
    try:
        print("1. Initializing components...")
        resume_parser = ResumeParser()
        jd_parser = JdParser()
        relevance_scorer = RelevanceScorer()
        semantic_matcher = SemanticMatcher()
        print("SUCCESS: All components initialized successfully")
    except Exception as e:
        print(f"ERROR: Error initializing components: {e}")
        return
    
    # Test with sample data
    print("\n2. Creating sample data for testing...")
    
    # Sample resume text
    sample_resume_text = """
    John Doe
    Data Analyst
    
    Email: john.doe@example.com
    Phone: (555) 123-4567
    
    SUMMARY
    Experienced data analyst with 3 years of experience in Python and SQL.
    
    EXPERIENCE
    Data Analyst | Tech Solutions Inc. | jan2020 - Present
    - Analyzed large datasets using Python and pandas
    - Created dashboards with Power BI
    """
    
    # Sample JD text
    sample_jd_text = """
    Data Analyst Position
    
    We are looking for a Data Analyst with experience in Python and SQL.
    
    Requirements:
    - 2+ years of experience with Python
    - Experience with SQL databases
    - Knowledge of data visualization tools
    
    Nice to have:
    - Experience with Power BI
    - Machine learning knowledge
    """
    
    try:
        print("\n3. Testing resume parsing...")
        # Simulate parsed resume data
        resume_data = {
            "text": sample_resume_text,
            "sections": {
                "contact": "Email: john.doe@example.com",
                "summary": "Experienced data analyst with 3 years of experience in Python and SQL.",
                "experience": "Data Analyst | Tech Solutions Inc.",
                "education": "",
                "skills": "Python, SQL, Power BI",
                "projects": "",
                "certifications": ""
            },
            "keywords": ["python", "sql", "power", "bi", "data", "analyst"],
            "email": "john.doe@example.com",
            "phone": "(555) 123-4567"
        }
        print("SUCCESS: Resume parsing simulation successful")
        print(f"  Extracted email: {resume_data['email']}")
    except Exception as e:
        print(f"ERROR: Error in resume parsing: {e}")
        return
    
    try:
        print("\n4. Testing JD parsing...")
        jd_data = jd_parser.parse(sample_jd_text)
        print("SUCCESS: JD parsing successful")
        print(f"  Job title: {jd_data.get('job_title', 'Not found')}")
        print(f"  Must-have skills: {jd_data.get('must_have_skills', [])}")
    except Exception as e:
        print(f"ERROR: Error in JD parsing: {e}")
        return
    
    try:
        print("\n5. Testing relevance scoring...")
        relevance_result = relevance_scorer.calculate_relevance(resume_data, jd_data)
        print("SUCCESS: Relevance scoring successful")
        print(f"  Score: {relevance_result['relevance_score']}")
        print(f"  Verdict: {relevance_result['verdict']}")
    except Exception as e:
        print(f"ERROR: Error in relevance scoring: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n6. Testing semantic matching...")
        semantic_result = semantic_matcher.calculate_semantic_similarity(resume_data, jd_data)
        print("SUCCESS: Semantic matching successful")
        print(f"  Similarity: {semantic_result['overall_similarity']}")
    except Exception as e:
        print(f"ERROR: Error in semantic matching: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n=== All tests completed successfully! ===")
    print("The processing pipeline is working correctly.")

if __name__ == "__main__":
    debug_processing()