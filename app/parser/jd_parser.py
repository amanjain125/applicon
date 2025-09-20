import re
from typing import Dict, List

class JdParser:
    """Parse job descriptions to extract key requirements"""
    
    def __init__(self):
        pass
    
    def parse(self, text: str) -> Dict[str, any]:
        """Parse job description text and extract key components"""
        # Extract job title
        job_title = self._extract_job_title(text)
        
        # Extract must-have skills
        must_have_skills = self._extract_must_have_skills(text)
        
        # Extract good-to-have skills
        good_to_have_skills = self._extract_good_to_have_skills(text)
        
        # Extract qualifications
        qualifications = self._extract_qualifications(text)
        
        # Extract experience requirements
        experience = self._extract_experience(text)
        
        # Extract keywords
        keywords = self._extract_keywords(text)
        
        return {
            "job_title": job_title,
            "must_have_skills": must_have_skills,
            "good_to_have_skills": good_to_have_skills,
            "qualifications": qualifications,
            "experience": experience,
            "keywords": keywords,
            "text": text
        }
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title from text"""
        # Look for explicit "Job Title" or similar patterns
        title_patterns = [
            r'(?:job\s+title|position|role)[:\s]*([^\n]+)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?:\s+Position|\s+Role)?$'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean up the title
                title = re.sub(r'^[^\w]*|[^\w]*$', '', title)  # Remove leading/trailing non-word chars
                if len(title) > 2 and len(title) < 100:
                    return title
        
        # Check first few lines for potential job titles
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            # If line is short and has title case words
            if len(line) < 50 and len(line) > 3 and line.istitle():
                # Make sure it's not a section header
                if not any(keyword in line.lower() for keyword in ['job description', 'requirements', 'responsibilities']):
                    return line
        
        return "Unknown Position"
    
    def _extract_must_have_skills(self, text: str) -> List[str]:
        """Extract must-have skills from job description"""
        skills = []
        
        # Common patterns for required skills
        patterns = [
            r"(?:must|should|required|necessary|essential).*?(?:have|possess|know|understand).*?:?\s*([^.]+)",
            r"(?:requirements|skills required|mandatory).*?:?\s*([^.]+)",
            r"(?:experience|proficiency|expertise).*?(?:in|with|of).*?:?\s*([^.]+)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                items = re.split(r'[,;]', match)
                for item in items:
                    item = item.strip()
                    if item and len(item) > 2:
                        # Clean up the item
                        item = re.sub(r'^[^\w]*|[^\w]*$', '', item)  # Remove leading/trailing non-word chars
                        if item and len(item) > 2:
                            skills.append(item)
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_good_to_have_skills(self, text: str) -> List[str]:
        """Extract good-to-have skills from job description"""
        skills = []
        
        # Common patterns for preferred skills
        patterns = [
            r"(?:nice|good|prefer|advantage).*?(?:to have|if).*?:?\s*([^.]+)",
            r"(?:preferred|bonus|extra|nice to have).*?:?\s*([^.]+)",
            r"(?:optional|desirable).*?:?\s*([^.]+)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                items = re.split(r'[,;]', match)
                for item in items:
                    item = item.strip()
                    if item and len(item) > 2:
                        # Clean up the item
                        item = re.sub(r'^[^\w]*|[^\w]*$', '', item)  # Remove leading/trailing non-word chars
                        if item and len(item) > 2:
                            skills.append(item)
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract educational qualifications from job description"""
        qualifications = []
        
        # Common patterns for qualifications
        patterns = [
            r"(?:degree|bachelor|master|phd|qualification).*?:?\s*([^.]+)",
            r"(?:education|educational).*?:?\s*([^.]+)",
            r"(?:academic).*?:?\s*([^.]+)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                items = re.split(r'[,;]', match)
                for item in items:
                    item = item.strip()
                    if item and len(item) > 2:
                        # Clean up the item
                        item = re.sub(r'^[^\w]*|[^\w]*$', '', item)  # Remove leading/trailing non-word chars
                        if item and len(item) > 2:
                            qualifications.append(item)
        
        return list(set(qualifications))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> str:
        """Extract experience requirements"""
        # Look for experience patterns
        patterns = [
            r"(\d+\+?\s*(?:years?|yrs?)\s*(?:experience|exp))",
            r"(?:experience.*?:?\s*(\d+\+?\s*(?:years?|yrs?)))",
            r"(\d+\+?\s*(?:years?|yrs?)\s*(?:of|in)\s*[a-z\s]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Not specified"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from job description"""
        # This is a simplified implementation
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        # Remove common stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 
                      'job', 'description', 'position', 'role', 'responsibilities', 'requirements', 'required', 'must', 'should',
                      'we', 'are', 'looking', 'for', 'a', 'an', 'this', 'that', 'these', 'those', 'have', 'has', 'had', 'do',
                      'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        keywords = [word for word in words if word not in stop_words]
        # Return unique keywords
        return list(set(keywords))