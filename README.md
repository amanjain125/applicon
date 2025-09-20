# Automated Resume Relevance Check System

An AI-powered system for automatically evaluating resumes against job descriptions, providing relevance scores and actionable feedback.

## Features

- Parse resumes (PDF/DOCX) and job descriptions (TXT)
- Calculate relevance scores using keyword matching and semantic analysis
- Generate personalized feedback for candidates
- Web dashboard for placement teams to view evaluations
- Store results in a database for future reference
- Batch processing of multiple resumes
- Email notifications (configurable)

## Quick Start (Local Development)

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the setup script (downloads required NLTK data):
   ```bash
   # On Windows
   setup.bat
   
   # On macOS/Linux
   chmod +x setup.sh
   ./setup.sh
   ```
4. Run the application:
   ```bash
   python app/api/app.py
   ```
5. Visit `http://localhost:5000` in your browser

## Usage

1. Navigate to the Upload page
2. Select a resume file (PDF or DOCX)
3. Select a job description file (TXT)
4. Click "Evaluate" to process the documents
5. View the relevance score, missing elements, and improvement suggestions

## Deployment (Public Access)

### Deploying to Render (Recommended)

1. Fork this repository to your GitHub account
2. Go to [Render](https://render.com/) and sign up for a free account
3. Click "New" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - Name: `resume-evaluator` (or any name you prefer)
   - Region: Select the closest region to you
   - Branch: `main` (or your default branch)
   - Root Directory: Leave empty
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/api/app.py`
6. Click "Create Web Service"
7. Wait for the deployment to complete (usually takes 5-10 minutes)
8. Once deployed, you'll get a public URL to access your application

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## API Endpoints

- `POST /api/evaluate` - Evaluate a resume against a job description
- `GET /api/evaluations` - Get all evaluations (with optional filtering)
- `GET /api/evaluations/<id>` - Get a specific evaluation
- `GET /api/statistics` - Get system statistics

## Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed information about:
- System architecture
- Scoring methodology
- Database schema
- Usage examples
- API endpoints

## Sample Data

Sample resumes and job descriptions can be found in the `samples` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Aman R Jain - Developer & Student