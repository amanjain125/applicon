from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import openai
import os

class SemanticMatcher:
    """Perform semantic matching between resume and job description using embeddings"""
    
    def __init__(self):
        # Initialize the sentence transformer model
        # Using a lightweight model for efficiency
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Try to get OpenAI API key from environment
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def calculate_semantic_similarity(self, resume_data: Dict, jd_data: Dict) -> Dict[str, float]:
        """Calculate semantic similarity between resume and job description"""
        
        # Get embeddings for resume and job description
        resume_embedding = self._get_resume_embedding(resume_data)
        jd_embedding = self._get_jd_embedding(jd_data)
        
        # Calculate cosine similarity
        similarity = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
        
        # Get section-wise similarities
        section_similarities = self._get_section_similarities(resume_data, jd_data)
        
        return {
            "overall_similarity": float(similarity),
            "section_similarities": section_similarities
        }
    
    def _get_resume_embedding(self, resume_data: Dict) -> np.ndarray:
        """Get embedding for resume text"""
        resume_text = resume_data.get("text", "")
        # Limit text length to prevent memory issues
        if len(resume_text) > 5000:
            resume_text = resume_text[:5000]
        return self.model.encode(resume_text)
    
    def _get_jd_embedding(self, jd_data: Dict) -> np.ndarray:
        """Get embedding for job description text"""
        jd_text = jd_data.get("text", "")
        # Limit text length to prevent memory issues
        if len(jd_text) > 5000:
            jd_text = jd_text[:5000]
        return self.model.encode(jd_text)
    
    def _get_section_similarities(self, resume_data: Dict, jd_data: Dict) -> Dict[str, float]:
        """Calculate similarity for key sections"""
        similarities = {}
        
        sections = ["experience", "skills", "education", "projects"]
        
        for section in sections:
            resume_section = resume_data.get("sections", {}).get(section, "")
            jd_section = ""  # In a real implementation, you might extract specific section from JD
            
            if resume_section:
                # For demo purposes, we'll compare resume sections with entire JD
                # In a production system, you'd extract corresponding sections from JD
                jd_text = jd_data.get("text", "")
                
                if len(resume_section) > 1000:
                    resume_section = resume_section[:1000]
                if len(jd_text) > 1000:
                    jd_text = jd_text[:1000]
                
                if resume_section and jd_text:
                    resume_emb = self.model.encode(resume_section)
                    jd_emb = self.model.encode(jd_text)
                    similarity = cosine_similarity([resume_emb], [jd_emb])[0][0]
                    similarities[section] = float(similarity)
        
        return similarities
    
    def get_improved_feedback(self, resume_data: Dict, jd_data: Dict) -> str:
        """Generate improved feedback using semantic understanding"""
        # If OpenAI API key is available, use GPT for feedback generation
        if self.openai_api_key:
            try:
                return self._generate_gpt_feedback(resume_data, jd_data)
            except Exception as e:
                print(f"Failed to generate GPT feedback: {e}")
                # Fall back to rule-based feedback
                return self._generate_rule_based_feedback(resume_data, jd_data)
        else:
            # Use rule-based feedback generation
            return self._generate_rule_based_feedback(resume_data, jd_data)
    
    def _generate_gpt_feedback(self, resume_data: Dict, jd_data: Dict) -> str:
        """Generate feedback using OpenAI GPT"""
        resume_text = resume_data.get("text", "")[:2000]  # Limit length
        jd_text = jd_data.get("text", "")[:2000]  # Limit length
        
        prompt = f"""
        As a resume expert, analyze the following resume against the job description.
        Provide specific, actionable feedback to improve the candidate's chances.
        
        Job Description:
        {jd_text}
        
        Resume:
        {resume_text}
        
        Please provide:
        1. A brief summary of the match quality (1-2 sentences)
        2. Three specific suggestions for improvement
        3. Any sections that are particularly strong
        """
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()
    
    def _generate_rule_based_feedback(self, resume_data: Dict, jd_data: Dict) -> str:
        """Generate feedback using rule-based approach"""
        # This is a simplified implementation
        # In a real system, you would use an LLM to generate detailed feedback
        
        feedback = "Based on semantic analysis:\n"
        
        # Get overall similarity
        semantic_result = self.calculate_semantic_similarity(resume_data, jd_data)
        overall_sim = semantic_result["overall_similarity"]
        
        if overall_sim > 0.8:
            feedback += "- Your resume content is highly relevant to this position.\n"
        elif overall_sim > 0.6:
            feedback += "- Your resume shows moderate relevance to this position.\n"
        else:
            feedback += "- Consider tailoring your resume more closely to this position.\n"
        
        # Add section-specific feedback
        section_sims = semantic_result["section_similarities"]
        for section, similarity in section_sims.items():
            if similarity < 0.5:
                feedback += f"- Your {section} section could be improved to better match the job requirements.\n"
        
        return feedback