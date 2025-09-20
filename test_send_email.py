import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import ResumeEvaluator

def test_send_email():
    print("=== Testing Email Sending ===")
    
    try:
        evaluator = ResumeEvaluator()
        print("Evaluator initialized.")
        
        # Get the latest evaluation ID
        evaluations = evaluator.get_evaluations()
        if evaluations:
            latest_eval = evaluations[0]  # First one is latest (ordered by timestamp DESC)
            eval_id = latest_eval['id']
            print(f"Latest evaluation ID: {eval_id}")
            print(f"Candidate email: {latest_eval.get('email', 'Not found')}")
            print(f"Candidate phone: {latest_eval.get('phone', 'Not found')}")
            
            # Try to send email
            print("Attempting to send email...")
            success = evaluator.send_evaluation_email(eval_id)
            if success:
                print("Email sent successfully!")
            else:
                print("Failed to send email")
        else:
            print("No evaluations found in database")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_send_email()