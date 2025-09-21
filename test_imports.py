import sys
import os

# Add the current directory and parent directories to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

print("Python path:", sys.path)
print("Current directory:", current_dir)
print("Parent directory:", parent_dir)

try:
    from app.main import ResumeEvaluator
    print("Successfully imported ResumeEvaluator")
except Exception as e:
    print(f"Failed to import ResumeEvaluator: {e}")
    import traceback
    traceback.print_exc()