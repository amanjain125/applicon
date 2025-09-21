# Automated Resume Relevance Check System

This is an AI-powered system for automatically evaluating resumes against job descriptions, providing relevance scores and actionable feedback.

## Deployment Instructions

### Deploying to Railway (Recommended for Size Constraints)

1. Fork this repository to your GitHub account
2. Go to [Railway](https://railway.app/) and sign up for a free account
3. Click "New Project" and select "Deploy from GitHub repo"
4. Connect your GitHub repository
5. Railway will auto-detect it's a Python app
6. In the settings, ensure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/api/app.py`
7. Add environment variables:
   - Key: `PORT`, Value: `8000`
8. Click "Deploy"
9. Your app will be live within minutes

### Deploying to Render

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

### Environment Variables (Optional)

If you want to configure email notifications:
- `EMAIL_ADDRESS`: Your email address for sending notifications
- `EMAIL_PASSWORD`: App password for your email account
- `EMAIL_SMTP_SERVER`: SMTP server (e.g., smtp.gmail.com)
- `EMAIL_SMTP_PORT`: SMTP port (e.g., 587)

For OpenAI feedback generation:
- `OPENAI_API_KEY`: Your OpenAI API key

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app/api/app.py
   ```

3. Visit `http://localhost:5000` in your browser

## Features

- Parse resumes (PDF/DOCX) and job descriptions (TXT)
- Calculate relevance scores using keyword matching and semantic analysis
- Generate personalized feedback for candidates
- Web dashboard for placement teams to view evaluations
- Store results in a database for future reference