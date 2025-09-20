from typing import Dict, List, Tuple
import re
from difflib import SequenceMatcher

class RelevanceScorer:
    """Calculate relevance score between resume and job description"""
    
    def __init__(self):
        # Weight distribution for scoring
        self.weights = {
            "must_have_skills": 0.4,
            "good_to_have_skills": 0.2,
            "qualifications": 0.15,
            "experience": 0.15,
            "keywords": 0.1
        }
    
    def calculate_relevance(self, resume_data: Dict, jd_data: Dict) -> Dict[str, any]:
        """Calculate overall relevance score and provide feedback"""
        
        # Calculate scores for each component
        must_have_score, missing_must_haves = self._score_must_have_skills(
            resume_data.get("keywords", []), 
            jd_data.get("must_have_skills", [])
        )
        
        good_to_have_score, missing_good_to_haves = self._score_good_to_have_skills(
            resume_data.get("keywords", []), 
            jd_data.get("good_to_have_skills", [])
        )
        
        qualification_score, missing_qualifications = self._score_qualifications(
            resume_data.get("sections", {}).get("education", ""), 
            jd_data.get("qualifications", [])
        )
        
        experience_score = self._score_experience(
            resume_data.get("sections", {}).get("experience", ""), 
            jd_data.get("experience", "")
        )
        
        keyword_score = self._score_keywords(
            resume_data.get("keywords", []), 
            jd_data.get("keywords", [])
        )
        
        # Calculate weighted score
        weighted_score = (
            must_have_score * self.weights["must_have_skills"] +
            good_to_have_score * self.weights["good_to_have_skills"] +
            qualification_score * self.weights["qualifications"] +
            experience_score * self.weights["experience"] +
            keyword_score * self.weights["keywords"]
        ) * 100
        
        # Determine verdict
        verdict = self._get_verdict(weighted_score)
        
        # Generate feedback
        feedback = self._generate_feedback(
            missing_must_haves, 
            missing_good_to_haves, 
            missing_qualifications,
            jd_data.get("experience", "")
        )
        
        return {
            "relevance_score": round(weighted_score, 2),
            "verdict": verdict,
            "missing_elements": {
                "must_have_skills": missing_must_haves,
                "good_to_have_skills": missing_good_to_haves,
                "qualifications": missing_qualifications
            },
            "feedback": feedback
        }
    
    def _score_must_have_skills(self, resume_keywords: List[str], jd_skills: List[str]) -> Tuple[float, List[str]]:
        """Score must-have skills match"""
        if not jd_skills:
            return 1.0, []  # No skills required
        
        matched = 0
        missing = []
        
        resume_keywords_lower = [k.lower() for k in resume_keywords]
        
        for skill in jd_skills:
            skill_lower = skill.lower()
            # Check for exact or fuzzy match
            if self._fuzzy_match(skill_lower, resume_keywords_lower):
                matched += 1
            else:
                missing.append(skill)
        
        return matched / len(jd_skills), missing
    
    def _score_good_to_have_skills(self, resume_keywords: List[str], jd_skills: List[str]) -> Tuple[float, List[str]]:
        """Score good-to-have skills match"""
        if not jd_skills:
            return 1.0, []  # No preferred skills
        
        matched = 0
        missing = []
        
        resume_keywords_lower = [k.lower() for k in resume_keywords]
        
        for skill in jd_skills:
            skill_lower = skill.lower()
            # Check for exact or fuzzy match
            if self._fuzzy_match(skill_lower, resume_keywords_lower):
                matched += 1
            else:
                missing.append(skill)
        
        # Good-to-have skills have less impact on score
        score = matched / len(jd_skills) if jd_skills else 1.0
        return score, missing
    
    def _score_qualifications(self, resume_education: str, jd_qualifications: List[str]) -> Tuple[float, List[str]]:
        """Score educational qualifications match"""
        if not jd_qualifications:
            return 1.0, []  # No qualifications required
        
        matched = 0
        missing = []
        
        education_lower = resume_education.lower()
        
        for qual in jd_qualifications:
            qual_lower = qual.lower()
            # Check for exact or partial match
            if qual_lower in education_lower:
                matched += 1
            else:
                missing.append(qual)
        
        return matched / len(jd_qualifications), missing
    
    def _score_experience(self, resume_experience: str, jd_experience: str) -> float:
        """Score experience match"""
        if not jd_experience or jd_experience == "Not specified":
            return 1.0  # No experience requirement
        
        # Extract required years from JD
        required_years = self._extract_years(jd_experience)
        if required_years is None:
            return 1.0  # Could not parse requirement
        
        # Extract candidate years from resume
        candidate_years = self._extract_years(resume_experience)
        if candidate_years is None:
            return 0.0  # Could not determine candidate experience
        
        # Score based on experience
        if candidate_years >= required_years:
            return 1.0
        elif candidate_years >= required_years * 0.75:
            return 0.75
        elif candidate_years >= required_years * 0.5:
            return 0.5
        else:
            return 0.25
    
    def _score_keywords(self, resume_keywords: List[str], jd_keywords: List[str]) -> float:
        """Score general keyword match"""
        if not jd_keywords:
            return 1.0
        
        matched = 0
        resume_keywords_lower = [k.lower() for k in resume_keywords]
        jd_keywords_lower = [k.lower() for k in jd_keywords]
        
        for keyword in jd_keywords_lower:
            if self._fuzzy_match(keyword, resume_keywords_lower):
                matched += 1
        
        return matched / len(jd_keywords)
    
    def _fuzzy_match(self, target: str, candidates: List[str]) -> bool:
        """Check for fuzzy match between target and candidates"""
        for candidate in candidates:
            # Exact match
            if target == candidate:
                return True
            # Similarity ratio
            similarity = SequenceMatcher(None, target, candidate).ratio()
            if similarity > 0.8:  # 80% similarity threshold
                return True
        return False
    
    def _extract_years(self, text: str) -> int:
        """Extract years from text"""
        match = re.search(r'(\d+)', text)
        if match:
            return int(match.group(1))
        return None
    
    def _get_verdict(self, score: float) -> str:
        """Determine suitability verdict based on score"""
        if score >= 80:
            return "High"
        elif score >= 60:
            return "Medium"
        else:
            return "Low"
    
    def _generate_feedback(self, missing_must_haves: List[str], missing_good_to_haves: List[str], 
                          missing_qualifications: List[str], required_experience: str) -> str:
        """Generate improvement feedback for candidate"""
        feedback_parts = []
        
        if missing_must_haves:
            feedback_parts.append(f"Missing required skills: {', '.join(missing_must_haves[:5])}")
        
        if missing_qualifications:
            feedback_parts.append(f"Missing qualifications: {', '.join(missing_qualifications)}")
        
        if required_experience and required_experience != "Not specified":
            feedback_parts.append(f"Experience requirement: {required_experience}")
        
        if missing_good_to_haves:
            feedback_parts.append(f"Consider adding these preferred skills: {', '.join(missing_good_to_haves[:3])}")
        
        if not feedback_parts:
            return "Your resume matches well with the job requirements. Well done!"
        
        return "To improve your chances: " + "; ".join(feedback_parts)