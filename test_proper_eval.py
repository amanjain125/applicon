import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import ResumeEvaluator

def test_evaluation_with_proper_files():
    print("=== Testing Evaluation with Proper File Formats ===")
    
    try:
        evaluator = ResumeEvaluator()
        print("Evaluator initialized.")
        
        # Check if sample files exist
        if not os.path.exists("sample_resume.docx"):
            print("Error: sample_resume.docx not found")
            return
            
        if not os.path.exists("sample_jd.txt"):
            print("Error: sample_jd.txt not found")
            return
        
        print("Testing evaluation...")
        result = evaluator.evaluate("sample_resume.docx", "sample_jd.txt")
        print("Evaluation successful!")
        print(f"Score: {result['relevance_score']}")
        print(f"Verdict: {result['verdict']}")
        print(f"Email: {result['email']}")
        print(f"Phone: {result['phone']}")
        print(f"Job Title: {result['job_title']}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_evaluation_with_proper_files()