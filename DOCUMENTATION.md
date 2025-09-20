# Automated Resume Relevance Check System

## Overview

This system automates the evaluation of resumes against job descriptions, providing a relevance score and actionable feedback. It's designed to help placement teams at Innomatics Research Labs efficiently process large volumes of applications.

## Features

- Parse resumes (PDF/DOCX) and job descriptions (TXT)
- Calculate relevance scores using keyword matching and semantic analysis
- Generate personalized feedback for candidates
- Web dashboard for placement teams to view evaluations
- Store results in a database for future reference

## System Architecture

```
app/
├── parser/              # Text extraction from documents
│   ├── resume_parser.py
│   └── jd_parser.py
├── scoring/             # Relevance scoring algorithms
│   ├── relevance_scorer.py
│   └── semantic_matcher.py
├── models/              # Database models
│   └── database.py
├── api/                 # Web application
│   └── app.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── upload.html
│   └── evaluation.html
├── main.py              # Main application orchestrator
└── utils/               # Utility functions

samples/                 # Sample data
uploads/                 # Uploaded files (temporary)
```

## Installation

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install flask pdfplumber python-docx docx2txt nltk sentence-transformers
   ```

## Running the Application

### Method 1: Using the run script (Windows)
```bash
run.bat
```

### Method 2: Direct command
```bash
python app/api/app.py
```

After starting the application, visit `http://localhost:5000` in your browser.

## Usage

1. Navigate to the Upload page
2. Select a resume file (PDF or DOCX)
3. Select a job description file (TXT)
4. Click "Evaluate" to process the documents
5. View the relevance score, missing elements, and improvement suggestions

## API Endpoints

- `POST /api/evaluate` - Evaluate a resume against a job description
- `GET /api/evaluations` - Get all evaluations (with optional filtering)
- `GET /api/evaluations/<id>` - Get a specific evaluation
- `GET /api/statistics` - Get system statistics

## Scoring Methodology

The system uses a hybrid approach to calculate relevance scores:

1. **Keyword Matching (40% weight)**: Exact and fuzzy matching of required skills
2. **Preferred Skills (20% weight)**: Matching of nice-to-have skills
3. **Qualifications (15% weight)**: Educational requirements match
4. **Experience (15% weight)**: Years of experience requirement
5. **Semantic Similarity (10% weight)**: Overall content similarity

Scores are normalized to a 0-100 scale with the following interpretations:
- 80-100: High suitability
- 60-79: Medium suitability
- 0-59: Low suitability

## Database Schema

The system uses SQLite for data storage with the following schema:

```sql
CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    resume_filename TEXT NOT NULL,
    jd_filename TEXT NOT NULL,
    job_title TEXT,
    relevance_score REAL,
    verdict TEXT,
    missing_elements TEXT,
    feedback TEXT,
    semantic_similarity REAL,
    resume_text TEXT,
    jd_text TEXT
);
```

## Sample Data

Sample resumes and job descriptions can be found in the `samples` directory.

## Troubleshooting

### Common Issues

1. **Installation errors**: Make sure you're using Python 3.8 or higher
2. **PDF parsing issues**: Ensure PDF files are not password-protected or corrupted
3. **Performance**: For large files, processing may take several seconds

### Support

For issues not covered in this documentation, please contact the development team.