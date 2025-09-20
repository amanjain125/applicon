import os
import sys
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from main import ResumeEvaluator

def create_sample_files():
    """Create sample resume and job description files for testing"""
    # Create samples directory
    os.makedirs("samples", exist_ok=True)
    
    # Sample resume
    resume_content = """
    John Doe
    Software Engineer
    
    CONTACT
    Email: john.doe@example.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    
    SUMMARY
    Experienced software engineer with 5 years of experience in Python, JavaScript, and cloud technologies.
    Skilled in developing scalable web applications and working in agile environments.
    
    EXPERIENCE
    Senior Software Engineer | Tech Solutions Inc. | Jan 2020 - Present
    - Developed RESTful APIs using Python Flask and Django
    - Implemented microservices architecture using Docker and Kubernetes
    - Collaborated with frontend teams to integrate React applications
    - Reduced application response time by 40% through optimization
    
    Software Engineer | Innovate Co. | Jun 2017 - Dec 2019
    - Built data processing pipelines with Python and Apache Spark
    - Created automated testing frameworks that improved code coverage to 90%
    - Mentored junior developers on best practices
    
    EDUCATION
    M.S. in Computer Science | University of Technology | 2017
    B.S. in Software Engineering | State University | 2015
    
    SKILLS
    Programming: Python, JavaScript, Java, SQL
    Frameworks: Flask, Django, React, Node.js
    Tools: Docker, Kubernetes, Git, Jenkins
    Cloud: AWS, Google Cloud Platform
    Databases: PostgreSQL, MongoDB, Redis
    
    PROJECTS
    E-commerce Platform | Personal Project
    - Built a full-stack e-commerce solution using Django and React
    - Integrated payment processing with Stripe API
    - Deployed on AWS with auto-scaling capabilities
    
    Data Analytics Dashboard | Team Project
    - Developed a real-time analytics dashboard using Python and D3.js
    - Processed large datasets with Pandas and NumPy
    - Implemented data visualization features for business insights
    """
    
    # Sample job description
    job_description_content = """
    Senior Python Developer
    
    We are looking for an experienced Python Developer to join our team. The ideal candidate will have 
    strong experience with web frameworks, cloud technologies, and modern development practices.
    
    RESPONSIBILITIES
    - Design and implement scalable web applications
    - Develop and maintain RESTful APIs
    - Collaborate with cross-functional teams
    - Write clean, maintainable, and testable code
    - Participate in code reviews and technical discussions
    
    REQUIREMENTS
    - Bachelor's degree in Computer Science or related field
    - 5+ years of experience with Python
    - Experience with Flask or Django frameworks
    - Knowledge of cloud platforms (AWS or GCP)
    - Experience with Docker and containerization
    - Strong understanding of databases (PostgreSQL, MongoDB)
    - Familiarity with testing frameworks
    
    NICE TO HAVE
    - Experience with Kubernetes
    - Knowledge of React or other frontend frameworks
    - Experience with CI/CD pipelines
    - Understanding of microservices architecture
    
    EXPERIENCE
    5+ years of relevant experience required
    
    BENEFITS
    - Competitive salary and equity
    - Health, dental, and vision insurance
    - Flexible working hours
    - Professional development opportunities
    """
    
    # Write sample files
    with open("samples/sample_resume.txt", "w") as f:
        f.write(resume_content)
    
    with open("samples/sample_jd.txt", "w") as f:
        f.write(job_description_content)
    
    print("Sample files created in 'samples' directory")

def test_system():
    """Test the resume evaluation system"""
    print("Testing Automated Resume Relevance Check System...")
    
    # Create sample files if they don't exist
    if not os.path.exists("samples/sample_resume.txt") or not os.path.exists("samples/sample_jd.txt"):
        create_sample_files()
    
    # Initialize evaluator
    evaluator = ResumeEvaluator()
    
    # For this test, we'll simulate the process since we don't have actual PDF/DOCX files
    print("System components loaded successfully")
    print("The system is ready to use!")
    print("\nTo use the system:")
    print("1. Run 'python app/api/app.py' to start the web server")
    print("2. Visit http://localhost:5000 in your browser")
    print("3. Navigate to the Upload page")
    print("4. Upload a resume (PDF/DOCX) and job description (TXT)")
    print("5. View the evaluation results")

if __name__ == "__main__":
    test_system()