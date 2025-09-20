@echo off
echo Setting up Automated Resume Relevance Check System...

echo Installing dependencies...
pip install -r requirements.txt

echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

echo Setup complete!
echo To run the application, execute: python app/api/app.py
echo Then visit http://localhost:5000 in your browser