# Automated Resume Relevance Check System - Project Summary

## Project Overview

We have successfully built a comprehensive Automated Resume Relevance Check System for Innomatics Research Labs. This system addresses the challenges of manual, inconsistent, and time-consuming resume evaluation by providing an automated solution that can scale to handle thousands of resumes weekly.

## Key Components Implemented

### 1. Document Parsing
- **Resume Parser**: Extracts text from PDF and DOCX resume files
- **Job Description Parser**: Processes job descriptions to identify key requirements

### 2. Relevance Scoring Engine
- **Keyword Matching**: Exact and fuzzy matching of required skills (40% weight)
- **Preferred Skills**: Matching of nice-to-have skills (20% weight)
- **Qualifications**: Educational requirements match (15% weight)
- **Experience**: Years of experience requirement (15% weight)
- **Semantic Similarity**: Overall content similarity using sentence transformers (10% weight)

### 3. Web Application
- **Flask Backend**: REST API for processing uploads and serving results
- **Dashboard Interface**: Web-based dashboard for placement teams
- **Upload Page**: Simple interface for uploading resumes and job descriptions
- **Evaluation Results**: Detailed scoring and feedback display

### 4. Data Storage
- **SQLite Database**: Persistent storage of evaluation results
- **Statistics Dashboard**: Overview of evaluation metrics

### 5. Advanced Features
- **Semantic Matching**: Uses sentence transformers for contextual understanding
- **Personalized Feedback**: Actionable suggestions for candidates
- **Scalable Architecture**: Designed to handle high volumes

## Technical Stack

- **Backend**: Python, Flask
- **Document Processing**: pdfplumber, python-docx, docx2txt
- **Natural Language Processing**: NLTK, sentence-transformers
- **Machine Learning**: scikit-learn
- **Frontend**: HTML, Bootstrap, jQuery
- **Database**: SQLite

## System Workflow

1. Placement team uploads job description
2. Students upload resumes
3. System parses both documents
4. Relevance analysis performed using hybrid approach
5. Results stored in database
6. Placement team accesses results via dashboard

## Deliverables

1. Complete source code in `app/` directory
2. Sample data in `samples/` directory
3. Documentation in `DOCUMENTATION.md`
4. README and LICENSE files
5. Run script for easy deployment
6. Requirements file for dependency management

## Usage Instructions

1. Install dependencies: `pip install flask pdfplumber python-docx docx2txt nltk sentence-transformers`
2. Run the application: `python app/api/app.py`
3. Access the web interface at `http://localhost:5000`

## Future Enhancements

1. Integration with cloud storage services
2. Advanced LLM integration for more sophisticated feedback
3. Multi-language support
4. Mobile-responsive design
5. Email notifications for evaluation results
6. Integration with applicant tracking systems (ATS)

This system provides a solid foundation for automating resume evaluation while maintaining flexibility for future enhancements.