import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, render_template, send_file
import json
from main import ResumeEvaluator
from werkzeug.utils import secure_filename
import traceback

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, '..', 'templates')
static_dir = os.path.join(current_dir, '..', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize evaluator
evaluator = ResumeEvaluator()

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_resume():
    """API endpoint to evaluate a resume against a job description"""
    try:
        print("=== Starting resume evaluation ===")
        
        # Check if files were uploaded
        if 'resume' not in request.files or 'jd' not in request.files:
            print("Error: Missing files in request")
            return jsonify({'error': 'Both resume and job description files are required'}), 400
        
        resume_file = request.files['resume']
        jd_file = request.files['jd']
        
        if resume_file.filename == '' or jd_file.filename == '':
            print("Error: Empty filenames")
            return jsonify({'error': 'Both resume and job description files are required'}), 400
        
        # Save files
        resume_filename = secure_filename(resume_file.filename)
        jd_filename = secure_filename(jd_file.filename)
        
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        
        print(f"Saving files: {resume_path}, {jd_path}")
        resume_file.save(resume_path)
        jd_file.save(jd_path)
        
        try:
            # Evaluate resume
            print("Starting evaluation...")
            result = evaluator.evaluate(resume_path, jd_path)
            print("Evaluation completed successfully")
            return jsonify(result)
        except Exception as e:
            print(f"Evaluation failed: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': f'Evaluation failed: {str(e)}'}), 500
        finally:
            # Clean up uploaded files
            try:
                os.remove(resume_path)
                os.remove(jd_path)
                print("Cleaned up uploaded files")
            except Exception as e:
                print(f"Failed to clean up files: {e}")
    except Exception as e:
        print(f"API endpoint failed: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'API processing failed: {str(e)}'}), 500

@app.route('/api/evaluations', methods=['GET'])
def get_evaluations():
    """API endpoint to get all evaluations"""
    job_title = request.args.get('job_title', None)
    min_score = request.args.get('min_score', None)
    
    if min_score is not None:
        try:
            min_score = float(min_score)
        except ValueError:
            min_score = None
    
    evaluations = evaluator.get_evaluations(job_title, min_score)
    return jsonify(evaluations)

@app.route('/api/evaluations/<int:evaluation_id>', methods=['GET'])
def get_evaluation(evaluation_id):
    """API endpoint to get a specific evaluation"""
    evaluation = evaluator.get_evaluation(evaluation_id)
    if evaluation:
        return jsonify(evaluation)
    else:
        return jsonify({'error': 'Evaluation not found'}), 404

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """API endpoint to get evaluation statistics"""
    try:
        stats = evaluator.get_statistics()
        print(f"API Statistics: {stats}")  # Debug print
        return jsonify(stats)
    except Exception as e:
        print(f"Error in statistics API: {e}")  # Debug print
        return jsonify({'error': f'Failed to get statistics: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Serve the main dashboard"""
    return render_template('dashboard.html')

@app.route('/upload')
def upload_page():
    """Serve the upload page"""
    return render_template('upload.html')

@app.route('/batch-upload')
def batch_upload_page():
    """Serve the batch upload page"""
    return render_template('batch_upload.html')

@app.route('/api/job-titles', methods=['GET'])
def get_job_titles():
    """API endpoint to get all unique job titles"""
    try:
        job_titles = evaluator.get_unique_job_titles()
        return jsonify({'job_titles': job_titles})
    except Exception as e:
        return jsonify({'error': f'Failed to get job titles: {str(e)}'}), 500

@app.route('/api/compare-candidates', methods=['GET'])
def compare_candidates():
    """API endpoint to get candidates for comparison"""
    job_title = request.args.get('job_title')
    if not job_title:
        return jsonify({'error': 'Job title is required'}), 400
    
    try:
        candidates = evaluator.get_candidates_for_comparison(job_title)
        return jsonify(candidates)
    except Exception as e:
        return jsonify({'error': f'Failed to get candidates: {str(e)}'}), 500

@app.route('/compare')
def comparison_page():
    """Serve the candidate comparison page"""
    job_title = request.args.get('job_title', '')
    return render_template('comparison.html', job_title=job_title)

@app.route('/evaluation/<int:evaluation_id>')
def evaluation_detail(evaluation_id):
    """Serve the evaluation detail page"""
    return render_template('evaluation.html', evaluation_id=evaluation_id)

@app.route('/api/batch-evaluate', methods=['POST'])
def batch_evaluate_resumes():
    """API endpoint to evaluate multiple resumes against a job description"""
    try:
        print("=== Starting batch evaluation ===")
        
        # Check if files were uploaded
        if 'jd' not in request.files:
            print("Error: Missing job description file")
            return jsonify({'error': 'Job description file is required'}), 400
        
        jd_file = request.files['jd']
        resume_files = request.files.getlist('resumes')
        
        # Check for send_emails parameter
        send_emails = request.form.get('send_emails', 'false').lower() == 'true'
        
        if jd_file.filename == '':
            print("Error: Empty job description filename")
            return jsonify({'error': 'Job description file is required'}), 400
        
        if not resume_files or len(resume_files) == 0:
            print("Error: No resume files provided")
            return jsonify({'error': 'At least one resume file is required'}), 400
        
        # Save job description
        jd_filename = secure_filename(jd_file.filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        print(f"Saving job description: {jd_path}")
        jd_file.save(jd_path)
        
        results = []
        resume_paths = []
        
        try:
            # Save all resume files first
            print(f"Saving {len(resume_files)} resume files...")
            for i, resume_file in enumerate(resume_files):
                if resume_file.filename != '':
                    # Save resume
                    resume_filename = secure_filename(resume_file.filename)
                    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
                    print(f"  Saving resume {i+1}: {resume_path}")
                    resume_file.save(resume_path)
                    resume_paths.append(resume_path)
            
            # Process all resumes
            print("Starting batch evaluation...")
            results = evaluator.batch_evaluate(resume_paths, jd_path, send_emails)
            print(f"Batch evaluation completed. Processed {len(results)} resumes.")
            
            return jsonify({
                'success': True,
                'results': results,
                'total_processed': len(results),
                'emails_sent': send_emails
            })
        except Exception as e:
            print(f"Batch processing failed: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': f'Batch processing failed: {str(e)}'}), 500
        finally:
            # Clean up job description file
            try:
                os.remove(jd_path)
                print("Cleaned up job description file")
            except Exception as e:
                print(f"Failed to clean up job description file: {e}")
            # Clean up resume files
            for resume_path in resume_paths:
                try:
                    os.remove(resume_path)
                    print(f"Cleaned up resume file: {resume_path}")
                except Exception as e:
                    print(f"Failed to clean up resume file {resume_path}: {e}")
    except Exception as e:
        print(f"Batch API endpoint failed: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Batch API processing failed: {str(e)}'}), 500

@app.route('/about')
def about_page():
    """Serve the about page"""
    return render_template('about.html')

@app.route('/api/send-email/<int:evaluation_id>', methods=['POST'])
def send_evaluation_email(evaluation_id):
    """API endpoint to send email for a specific evaluation"""
    try:
        success = evaluator.send_evaluation_email(evaluation_id)
        if success:
            return jsonify({'success': True, 'message': 'Email sent successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send email'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

if __name__ == '__main__':
    # Use the PORT environment variable if provided (for Render/Heroku), otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)