import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from parser.jd_parser import JdParser
from scoring.relevance_scorer import RelevanceScorer
from scoring.semantic_matcher import SemanticMatcher
from models.database import EvaluationDatabase
from services.email_service import EmailService

def debug_core_components():
    print("=== Debugging Core Components ===")
    
    try:
        print("1. Initializing components...")
        jd_parser = JdParser()
        relevance_scorer = RelevanceScorer()
        semantic_matcher = SemanticMatcher()
        database = EvaluationDatabase()
        email_service = EmailService()
        print("SUCCESS: All components initialized")
    except Exception as e:
        print(f"ERROR: Error initializing components: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test with sample data
    print("\n2. Creating sample data for testing...")
    
    # Sample resume data (simulated parsed data)
    resume_data = {
        "text": """John Doe
Data Analyst

Email: john.doe@example.com
Phone: (555) 123-4567

SUMMARY
Experienced data analyst with 3 years of experience in Python and SQL.

EXPERIENCE
Data Analyst | Tech Solutions Inc. | jan2020 - Present
- Analyzed large datasets using Python and pandas
- Created dashboards with Power BI
""",
        "sections": {
            "contact": "Email: john.doe@example.com",
            "summary": "Experienced data analyst with 3 years of experience in Python and SQL.",
            "experience": "Data Analyst | Tech Solutions Inc. | jan2020 - Present",
            "education": "",
            "skills": "Python, SQL, Power BI",
            "projects": "",
            "certifications": ""
        },
        "keywords": ["python", "sql", "power", "bi", "data", "analyst"],
        "email": "john.doe@example.com",
        "phone": "(555) 123-4567"
    }
    
    # Sample JD text
    jd_text = """Data Analyst Position

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
        print("\n3. Testing JD parsing...")
        jd_data = jd_parser.parse(jd_text)
        print("SUCCESS: JD parsing successful")
        print(f"  Job title: {jd_data.get('job_title', 'Not found')}")
        print(f"  Must-have skills: {jd_data.get('must_have_skills', [])}")
    except Exception as e:
        print(f"ERROR: Error in JD parsing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n4. Testing relevance scoring...")
        relevance_result = relevance_scorer.calculate_relevance(resume_data, jd_data)
        print("SUCCESS: Relevance scoring successful")
        print(f"  Score: {relevance_result['relevance_score']}")
        print(f"  Verdict: {relevance_result['verdict']}")
        print(f"  Missing elements: {list(relevance_result['missing_elements'].keys())}")
    except Exception as e:
        print(f"ERROR: Error in relevance scoring: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n5. Testing semantic matching...")
        semantic_result = semantic_matcher.calculate_semantic_similarity(resume_data, jd_data)
        print("SUCCESS: Semantic matching successful")
        print(f"  Similarity: {semantic_result['overall_similarity']}")
    except Exception as e:
        print(f"ERROR: Error in semantic matching: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n6. Testing database operations...")
        # Create a test evaluation result
        evaluation_result = {
            "resume_filename": "sample_resume.pdf",
            "jd_filename": "sample_jd.txt",
            "job_title": jd_data.get("job_title", "Unknown Position"),
            "relevance_score": relevance_result["relevance_score"],
            "verdict": relevance_result["verdict"],
            "missing_elements": relevance_result["missing_elements"],
            "feedback": relevance_result["feedback"],
            "semantic_similarity": semantic_result["overall_similarity"],
            "resume_text": resume_data["text"],
            "jd_text": jd_data["text"],
            "email": resume_data.get("email", ""),
            "phone": resume_data.get("phone", "")
        }
        
        evaluation_id = database.save_evaluation(evaluation_result)
        print("SUCCESS: Database operations successful")
        print(f"  Saved evaluation with ID: {evaluation_id}")
        
        # Retrieve the evaluation
        retrieved = database.get_evaluation_by_id(evaluation_id)
        if retrieved:
            print("SUCCESS: Successfully retrieved evaluation from database")
            print(f"  Retrieved job title: {retrieved.get('job_title', 'Not found')}")
            print(f"  Retrieved score: {retrieved.get('relevance_score', 'Not found')}")
        else:
            print("ERROR: Failed to retrieve evaluation from database")
    except Exception as e:
        print(f"ERROR: Error in database operations: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n7. Testing email service...")
        print(f"Email service configured: {email_service.is_configured()}")
        if email_service.is_configured():
            print("SUCCESS: Email service is configured")
            # Test sending email (but don't actually send)
            print("  Would send email to:", evaluation_result.get("email", "No email"))
        else:
            print("INFO: Email service is not configured (this is OK for debugging)")
    except Exception as e:
        print(f"ERROR: Error in email service: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n=== All core component tests completed! ===")
    print("The core pipeline is working correctly.")

if __name__ == "__main__":
    debug_core_components()