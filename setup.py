import os
import nltk
import spacy
from app.models.database import EvaluationDatabase

def setup_environment():
    """Set up the environment for the resume evaluation system"""
    print("Setting up Automated Resume Relevance Check System...")
    
    # Create necessary directories
    directories = ['uploads', 'samples']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Initialize database
    print("Initializing database...")
    db = EvaluationDatabase()
    print("Database initialized successfully")
    
    # Download NLTK data
    print("Downloading NLTK data...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("NLTK data downloaded successfully")
    except Exception as e:
        print(f"Warning: Failed to download NLTK data: {e}")
    
    # Download spaCy model
    print("Checking spaCy model...")
    try:
        spacy.load("en_core_web_sm")
        print("spaCy model is already installed")
    except OSError:
        print("spaCy model not found. Please install it with:")
        print("python -m spacy download en_core_web_sm")
    
    print("\nSetup complete!")
    print("To run the application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download spaCy model if not already installed")
    print("3. Run: python app/api/app.py")
    print("4. Access the web interface at http://localhost:5000")

if __name__ == "__main__":
    setup_environment()