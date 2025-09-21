import nltk
import ssl
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Try to download required NLTK data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    print(f"Warning: Failed to download NLTK data: {e}")

# Use relative imports
from app.parser.resume_parser import ResumeParser
from app.parser.jd_parser import JdParser
from app.scoring.relevance_scorer import RelevanceScorer
from app.scoring.semantic_matcher import SemanticMatcher
from app.models.database import EvaluationDatabase
from app.services.email_service import EmailService
from typing import Dict, List

class ResumeEvaluator:
    """Main orchestrator for resume evaluation"""
    
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.jd_parser = JdParser()
        self.relevance_scorer = RelevanceScorer()
        self.semantic_matcher = SemanticMatcher()
        self.database = EvaluationDatabase()
        self.email_service = EmailService()
        print("Applicon Resume Evaluator initialized successfully")
    
    def evaluate(self, resume_path: str, jd_path: str) -> Dict:
        """Evaluate a resume against a job description"""
        # Parse resume
        print(f"Parsing resume: {resume_path}")
        resume_data = self.resume_parser.parse(resume_path)
        
        # Parse job description
        print(f"Parsing job description: {jd_path}")
        try:
            with open(jd_path, 'r', encoding='utf-8') as f:
                jd_text = f.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(jd_path, 'r', encoding='latin-1') as f:
                jd_text = f.read()
        jd_data = self.jd_parser.parse(jd_text)
        
        # Use job title from JD, but if not found, try to infer from resume
        job_title = jd_data.get("job_title", "Unknown Position")
        if job_title == "Unknown Position" or job_title == "":
            # Try to use resume's inferred job title
            resume_job_title = resume_data.get("job_title", "General Applicant")
            if resume_job_title and resume_job_title != "General Applicant":
                job_title = resume_job_title
            else:
                job_title = "General Applicant"
        
        # Calculate relevance score
        print("Calculating relevance score...")
        relevance_result = self.relevance_scorer.calculate_relevance(resume_data, jd_data)
        
        # Calculate semantic similarity
        print("Calculating semantic similarity...")
        semantic_result = self.semantic_matcher.calculate_semantic_similarity(resume_data, jd_data)
        
        # Generate improved feedback
        print("Generating feedback...")
        improved_feedback = self.semantic_matcher.get_improved_feedback(resume_data, jd_data)
        
        # Combine results
        evaluation_result = {
            "resume_filename": os.path.basename(resume_path),
            "jd_filename": os.path.basename(jd_path),
            "job_title": job_title,
            "relevance_score": relevance_result["relevance_score"],
            "verdict": relevance_result["verdict"],
            "missing_elements": relevance_result["missing_elements"],
            "feedback": relevance_result["feedback"],
            "improved_feedback": improved_feedback,
            "semantic_similarity": semantic_result["overall_similarity"],
            "section_similarities": semantic_result["section_similarities"],
            "resume_text": resume_data["text"],
            "jd_text": jd_data["text"],
            "email": resume_data.get("email", ""),
            "phone": resume_data.get("phone", "")
        }
        
        # Save to database
        print("Saving evaluation to database...")
        evaluation_id = self.database.save_evaluation(evaluation_result)
        evaluation_result["evaluation_id"] = evaluation_id
        
        return evaluation_result
    
    def batch_evaluate(self, resume_paths: List[str], jd_path: str, send_emails: bool = False) -> List[Dict]:
        """Evaluate multiple resumes against a single job description"""
        results = []
        for resume_path in resume_paths:
            try:
                result = self.evaluate(resume_path, jd_path)
                results.append(result)
            except Exception as e:
                results.append({
                    "resume_filename": os.path.basename(resume_path),
                    "error": str(e)
                })
        
        # Send emails if requested
        if send_emails and self.email_service.is_configured():
            print("Sending feedback emails to candidates...")
            email_results = self.email_service.send_batch_feedback_emails(results)
            print(f"Email sending complete: {email_results['success_count']} successful, {email_results['failure_count']} failed")
        
        return results
    
    def send_evaluation_email(self, evaluation_id: int) -> bool:
        """Send email for a specific evaluation"""
        evaluation = self.get_evaluation(evaluation_id)
        if evaluation and self.email_service.is_configured():
            return self.email_service.send_feedback_email(evaluation)
        return False
    
    def get_evaluations(self, job_title: str = None, min_score: float = None) -> list:
        """Retrieve evaluations from database"""
        return self.database.get_evaluations(job_title, min_score)
    
    def get_evaluation(self, evaluation_id: int) -> dict:
        """Retrieve a specific evaluation"""
        return self.database.get_evaluation_by_id(evaluation_id)
    
    def get_candidates_for_comparison(self, job_title: str, limit: int = 5) -> List[Dict]:
        """Get top candidates for a specific job title for comparison"""
        return self.database.compare_candidates(job_title, limit)
    
    def get_unique_job_titles(self) -> List[str]:
        """Get all unique job titles from evaluations"""
        return self.database.get_unique_job_titles()
    
    def get_statistics(self) -> dict:
        """Get evaluation statistics"""
        try:
            stats = self.database.get_statistics()
            print(f"Main app statistics: {stats}")  # Debug print
            return stats
        except Exception as e:
            print(f"Error in main app statistics: {e}")  # Debug print
            raise
    
    def send_evaluation_email(self, evaluation_id: int) -> bool:
        """Send email for a specific evaluation"""
        try:
            evaluation = self.get_evaluation(evaluation_id)
            if evaluation:
                print(f"Found evaluation: {evaluation_id}")
                print(f"Candidate email: {evaluation.get('email', 'Not found')}")
                print(f"Candidate phone: {evaluation.get('phone', 'Not found')}")
                if self.email_service.is_configured():
                    success = self.email_service.send_feedback_email(evaluation)
                    print(f"Email sending result: {success}")
                    return success
                else:
                    print("Email service not configured")
                    return False
            else:
                print(f"Evaluation {evaluation_id} not found")
                return False
        except Exception as e:
            print(f"Error sending email: {e}")
            import traceback
            traceback.print_exc()
            return False
        except Exception as e:
            print(f"Error sending evaluation email: {e}")
            return False

# Example usage
if __name__ == "__main__":
    evaluator = ResumeEvaluator()
    
    # This would be called when processing files
    # result = evaluator.evaluate("sample_resume.pdf", "sample_jd.txt")
    # print(result)