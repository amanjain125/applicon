@echo off
echo Starting Automated Resume Relevance Check System...
echo.
echo Make sure you have installed the required dependencies:
echo pip install flask pdfplumber python-docx docx2txt nltk sentence-transformers
echo.
echo Starting the web server...
echo Visit http://localhost:5000 in your browser
echo.
python app/api/app.py