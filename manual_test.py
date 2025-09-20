# Manual Test Script

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import ResumeEvaluator

def manual_test():
    print("=== Manual Test ===")
    
    # Test the components individually first
    print("Testing individual components...")
    
    try:
        from parser.resume_parser import ResumeParser
        from parser.jd_parser import JdParser
        from scoring.relevance_scorer import RelevanceScorer
        from scoring.semantic_matcher import SemanticMatcher
        
        print("SUCCESS: All components imported successfully")
        
        # Test with sample data directly
        print("\nTesting with sample data...")
        
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
        
        # Sample JD data
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
        
        # Parse JD
        jd_parser = JdParser()
        jd_data = jd_parser.parse(jd_text)
        print("SUCCESS: JD parsing successful")
        print(f"  Job title: {jd_data.get('job_title', 'Not found')}")
        
        # Test relevance scoring
        relevance_scorer = RelevanceScorer()
        relevance_result = relevance_scorer.calculate_relevance(resume_data, jd_data)
        print("SUCCESS: Relevance scoring successful")
        print(f"  Score: {relevance_result['relevance_score']}")
        print(f"  Verdict: {relevance_result['verdict']}")
        
        # Test semantic matching
        semantic_matcher = SemanticMatcher()
        semantic_result = semantic_matcher.calculate_semantic_similarity(resume_data, jd_data)
        print("SUCCESS: Semantic matching successful")
        print(f"  Similarity: {semantic_result['overall_similarity']}")
        
        print("\n=== Component tests completed successfully! ===")
        
    except Exception as e:
        print(f"Error during component testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_test()