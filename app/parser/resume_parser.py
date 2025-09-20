import pdfplumber
import docx2txt
import re
from typing import Dict, List

class ResumeParser:
    """Parse resumes from PDF and DOCX formats"""
    
    def __init__(self):
        pass
    
    def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF resume"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        
        return text
    
    def parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX resume"""
        try:
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""
    
    def extract_email(self, text: str) -> str:
        """Extract email address from resume text"""
        # Regular expression for email matching
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from resume text"""
        # Regular expression for phone number matching (international format)
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return ""
    
    def extract_job_title(self, text: str) -> str:
        """Extract potential job title from resume"""
        # Look for common job title patterns
        lines = text.split('\n')
        
        # Check first few lines for potential job titles
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            # Skip if it looks like a name (typically the first line)
            if i == 0 and line.count(' ') < 3 and len(line) > 0:
                continue
                
            # Check if line looks like a job title (title case, reasonable length)
            if (len(line) > 3 and len(line) < 50 and 
                line.istitle() and 
                not any(keyword in line.lower() for keyword in ['email', 'phone', 'linkedin', 'address'])):
                return line
        
        # If no clear job title found, try to infer from experience section
        experience_match = re.search(r'(experience|work history|employment).*?(?=\n\n|\Z)', text, re.IGNORECASE)
        if experience_match:
            exp_text = experience_match.group(0)
            # Look for job titles in experience section
            job_title_patterns = [
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\|',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+at',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),'
            ]
            
            for pattern in job_title_patterns:
                matches = re.findall(pattern, exp_text)
                if matches:
                    return matches[0]
        
        return "General Applicant"
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract common resume sections"""
        sections = {
            "contact": "",
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "projects": "",
            "certifications": ""
        }
        
        # Normalize text by removing extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Define section headers patterns
        patterns = {
            "contact": r"(contact|address|phone|email|linkedin)[:\n\s]*.*?(?=\n\n|\Z)",
            "summary": r"(summary|objective|profile)[:\n\s]*.*?(?=\n\n|\Z)",
            "experience": r"(experience|work history|employment)[:\n\s]*.*?(?=\n\n|\Z)",
            "education": r"(education|academic)[:\n\s]*.*?(?=\n\n|\Z)",
            "skills": r"(skills|technical skills|expertise)[:\n\s]*.*?(?=\n\n|\Z)",
            "projects": r"(projects|personal projects)[:\n\s]*.*?(?=\n\n|\Z)",
            "certifications": r"(certifications|certificates)[:\n\s]*.*?(?=\n\n|\Z)"
        }
        
        # Extract sections using patterns
        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                sections[section] = match.group(0)
        
        return sections
    
    def parse_from_text(self, text: str) -> Dict[str, any]:
        """Parse resume from text content"""
        # Extract sections
        sections = self.extract_sections(text)
        
        # Extract contact information
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        
        # Extract potential job title
        job_title = self.extract_job_title(text)
        
        # Extract keywords and entities (simplified)
        keywords = self._extract_keywords(text)
        
        return {
            "text": text,
            "sections": sections,
            "keywords": keywords,
            "email": email,
            "phone": phone,
            "job_title": job_title
        }
    
    def parse(self, file_path: str) -> Dict[str, any]:
        """Main parsing function that determines file type and extracts content"""
        if file_path.lower().endswith('.pdf'):
            text = self.parse_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = self.parse_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
        
        # Extract sections
        sections = self.extract_sections(text)
        
        # Extract contact information
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        
        # Extract potential job title
        job_title = self.extract_job_title(text)
        
        # Extract keywords and entities (simplified)
        keywords = self._extract_keywords(text)
        
        return {
            "text": text,
            "sections": sections,
            "keywords": keywords,
            "email": email,
            "phone": phone,
            "job_title": job_title
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text (simplified implementation)"""
        # This is a placeholder - in a real implementation, you'd use NLP techniques
        # like spaCy or NLTK for entity extraction
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        # Remove common stop words (simplified)
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'i', 'have', 'am', 'my', 'me', 'as', 'a', 'an', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        keywords = [word for word in words if word not in stop_words]
        # Return unique keywords
        return list(set(keywords))