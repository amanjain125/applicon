import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from parser.resume_parser import ResumeParser
from parser.jd_parser import JdParser
from scoring.relevance_scorer import RelevanceScorer
from scoring.semantic_matcher import SemanticMatcher
from models.database import EvaluationDatabase
from services.email_service import EmailService

def debug_full_pipeline():
    print("=== Debugging Full Pipeline ===")
    
    try:
        print("1. Initializing all components...")
        resume_parser = ResumeParser()
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
    
    # Test with sample files
    print("\n2. Looking for sample files...")
    
    # Check if sample files exist
    sample_resume = "samples/sample_resume.txt"
    sample_jd = "samples/sample_jd.txt"
    
    if not os.path.exists(sample_resume):
        print(f"Creating sample resume file: {sample_resume}")
        with open(sample_resume, "w") as f:
            f.write("""
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
            """)
    
    if not os.path.exists(sample_jd):
        print(f"Creating sample JD file: {sample_jd}")
        with open(sample_jd, "w") as f:
            f.write("""
            Data Analyst Position
            
            We are looking for a Data Analyst with experience in Python and SQL.
            
            Requirements:
            - 2+ years of experience with Python
            - Experience with SQL databases
            - Knowledge of data visualization tools
            
            Nice to have:
            - Experience with Power BI
            - Machine learning knowledge
            """)
    
    try:
        print("\n3. Testing resume parsing...")
        resume_data = resume_parser.parse(sample_resume)
        print("SUCCESS: Resume parsing successful")
        print(f"  Email extracted: {resume_data.get('email', 'Not found')}")
        print(f"  Phone extracted: {resume_data.get('phone', 'Not found')}")
    except Exception as e:
        print(f"ERROR: Error in resume parsing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n4. Testing JD parsing...")
        with open(sample_jd, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        jd_data = jd_parser.parse(jd_text)
        print("SUCCESS: JD parsing successful")
        print(f"  Job title: {jd_data.get('job_title', 'Not found')}")
    except Exception as e:
        print(f"ERROR: Error in JD parsing: {e}")
        import traceback
        traceback.print_exc()
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
    
    try:
        print("\n7. Testing database operations...")
        # Create a test evaluation result
        evaluation_result = {
            "resume_filename": "sample_resume.txt",
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
        else:
            print("ERROR: Failed to retrieve evaluation from database")
    except Exception as e:
        print(f"ERROR: Error in database operations: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        print("\n8. Testing email service...")
        if email_service.is_configured():
            print("SUCCESS: Email service is configured")
            # We won't actually send an email in this debug test
        else:
            print("INFO: Email service is not configured (this is OK for debugging)")
    except Exception as e:
        print(f"ERROR: Error in email service: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n=== All debug tests completed! ===")
    print("The full pipeline is working correctly.")

if __name__ == "__main__":
    debug_full_pipeline()