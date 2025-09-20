import sqlite3
from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import base64

class EvaluationDatabase:
    """Handle database operations for storing evaluation results"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use absolute path for database to work in deployment
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'evaluations.db')
        else:
            self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create evaluations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
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
                jd_text TEXT,
                candidate_email TEXT,
                candidate_phone TEXT
            )
        ''')
        
        # Check if candidate_email column exists, if not add it
        cursor.execute("PRAGMA table_info(evaluations)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'candidate_email' not in columns:
            try:
                cursor.execute("ALTER TABLE evaluations ADD COLUMN candidate_email TEXT")
                print("Added candidate_email column")
            except sqlite3.OperationalError as e:
                print(f"Error adding candidate_email column: {e}")
        
        if 'candidate_phone' not in columns:
            try:
                cursor.execute("ALTER TABLE evaluations ADD COLUMN candidate_phone TEXT")
                print("Added candidate_phone column")
            except sqlite3.OperationalError as e:
                print(f"Error adding candidate_phone column: {e}")
        
        # Create indexes for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_job_title ON evaluations(job_title)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_score ON evaluations(relevance_score)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_evaluation(self, evaluation_data: Dict) -> int:
        """Save evaluation result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert missing_elements to JSON string
        missing_elements_json = json.dumps(evaluation_data.get("missing_elements", {}))
        
        cursor.execute('''
            INSERT INTO evaluations 
            (resume_filename, jd_filename, job_title, relevance_score, verdict, 
             missing_elements, feedback, semantic_similarity, resume_text, jd_text,
             candidate_email, candidate_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            evaluation_data.get("resume_filename", ""),
            evaluation_data.get("jd_filename", ""),
            evaluation_data.get("job_title", ""),
            evaluation_data.get("relevance_score", 0),
            evaluation_data.get("verdict", ""),
            missing_elements_json,
            evaluation_data.get("feedback", ""),
            evaluation_data.get("semantic_similarity", 0),
            evaluation_data.get("resume_text", ""),
            evaluation_data.get("jd_text", ""),
            evaluation_data.get("email", ""),
            evaluation_data.get("phone", "")
        ))
        
        evaluation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return evaluation_id
    
    def get_evaluations(self, job_title: Optional[str] = None, 
                       min_score: Optional[float] = None) -> List[Dict]:
        """Retrieve evaluations with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM evaluations WHERE 1=1"
        params = []
        
        # Add filters
        if job_title:
            query += " AND job_title LIKE ?"
            params.append(f"%{job_title}%")
        
        if min_score is not None:
            query += " AND relevance_score >= ?"
            params.append(min_score)
        
        # Order by timestamp (newest first)
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert to list of dictionaries
        evaluations = []
        for row in rows:
            evaluation = dict(zip(columns, row))
            # Convert missing_elements back from JSON
            try:
                evaluation["missing_elements"] = json.loads(evaluation["missing_elements"])
            except:
                evaluation["missing_elements"] = {}
            
            # Map database column names to expected field names
            if "candidate_email" in evaluation:
                evaluation["email"] = evaluation["candidate_email"]
            if "candidate_phone" in evaluation:
                evaluation["phone"] = evaluation["candidate_phone"]
            
            evaluations.append(evaluation)
        
        conn.close()
        return evaluations
    
    def get_evaluation_by_id(self, evaluation_id: int) -> Optional[Dict]:
        """Retrieve a specific evaluation by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM evaluations WHERE id = ?", (evaluation_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        evaluation = dict(zip(columns, row))
        
        # Convert missing_elements back from JSON
        try:
            evaluation["missing_elements"] = json.loads(evaluation["missing_elements"])
        except:
            evaluation["missing_elements"] = {}
        
        # Map database column names to expected field names
        if "candidate_email" in evaluation:
            evaluation["email"] = evaluation["candidate_email"]
        if "candidate_phone" in evaluation:
            evaluation["phone"] = evaluation["candidate_phone"]
        
        conn.close()
        return evaluation
    
    def get_evaluations_by_job_title(self, job_title: str) -> List[Dict]:
        """Retrieve all evaluations for a specific job title"""
        return self.get_evaluations(job_title=job_title)
    
    def compare_candidates(self, job_title: str, limit: int = 5) -> List[Dict]:
        """Get top candidates for a specific job title for comparison"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get top evaluations for this job title
        query = """
            SELECT * FROM evaluations 
            WHERE job_title = ? 
            ORDER BY relevance_score DESC 
            LIMIT ?
        """
        
        cursor.execute(query, (job_title, limit))
        rows = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert to list of dictionaries
        evaluations = []
        for row in rows:
            evaluation = dict(zip(columns, row))
            # Convert missing_elements back from JSON
            try:
                evaluation["missing_elements"] = json.loads(evaluation["missing_elements"])
            except:
                evaluation["missing_elements"] = {}
            evaluations.append(evaluation)
        
        conn.close()
        return evaluations
    
    def get_unique_job_titles(self) -> List[str]:
        """Get all unique job titles from evaluations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT job_title FROM evaluations WHERE job_title IS NOT NULL AND job_title != ''")
        rows = cursor.fetchall()
        
        job_titles = []
        for row in rows:
            title = row[0]
            # Filter out corrupted or invalid titles
            if (title and isinstance(title, str) and 
                len(title.strip()) > 0 and 
                len(title.strip()) < 100 and  # Reasonable length
                all(ord(char) < 128 for char in title) and  # ASCII only for now
                not title.startswith('%')):  # Filter out binary data
                clean_title = title.strip()
                # Remove any non-printable characters
                clean_title = ''.join(char for char in clean_title if char.isprintable())
                if len(clean_title) > 0 and len(clean_title) < 100:
                    job_titles.append(clean_title)
        
        conn.close()
        return job_titles
    
    def delete_evaluation(self, evaluation_id: int) -> bool:
        """Delete an evaluation by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM evaluations WHERE id = ?", (evaluation_id,))
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total evaluations
        cursor.execute("SELECT COUNT(*) FROM evaluations")
        total = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("SELECT AVG(relevance_score) FROM evaluations")
        avg_score = cursor.fetchone()[0]
        
        # Score distribution
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN relevance_score >= 80 THEN 1 END) as high,
                COUNT(CASE WHEN relevance_score >= 60 AND relevance_score < 80 THEN 1 END) as medium,
                COUNT(CASE WHEN relevance_score < 60 THEN 1 END) as low
            FROM evaluations
        """)
        distribution = cursor.fetchone()
        
        # Unique job titles
        cursor.execute("SELECT COUNT(DISTINCT job_title) FROM evaluations")
        unique_jobs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_evaluations": total or 0,
            "average_score": round(avg_score or 0, 2),
            "score_distribution": {
                "high": distribution[0] or 0,
                "medium": distribution[1] or 0,
                "low": distribution[2] or 0
            },
            "unique_job_titles": unique_jobs or 0
        }