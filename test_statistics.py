import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import ResumeEvaluator

def test_statistics():
    print("=== Testing Statistics ===")
    
    try:
        evaluator = ResumeEvaluator()
        stats = evaluator.get_statistics()
        print(f"Statistics: {stats}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_statistics()