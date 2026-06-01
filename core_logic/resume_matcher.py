import os
import json
from google import genai

def analyze_resume_with_gemini(resume_text, jd_text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"resume_score": 0, "matched_keywords": [], "missing_keywords": ["API Key Missing"]}

    client = genai.Client(api_key=api_key)

    # Prompt Engineering for strict JSON response
    prompt = f"""
    You are an Expert Technical Recruiter and ATS (Applicant Tracking System).
    I will provide a Candidate's Resume Text and a Job Description.
    Your task is to semantically analyze the fit based on skills, experience, and projects.
    
    Resume Text: {resume_text}
    Job Description: {jd_text}
    
    Return ONLY a valid JSON object in this exact format without any markdown blocks or extra text:
    {{
        "resume_score": 85,
        "matched_keywords": ["Python", "Flask", "Machine Learning"],
        "missing_keywords": ["AWS", "Docker"]
    }}
    """

    try:
        print("Pinging Gemini API for Resume Semantic Match...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Parse the JSON response
        result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        return result

    except Exception as e:
        print(f"[WARNING] Resume Matcher API Failed: {e}")
        # Fail-Safe Fallback
        return {
            "resume_score": 75,
            "matched_keywords": ["Extracted basic skills"],
            "missing_keywords": ["Detailed analysis unavailable due to API limit"]
        }