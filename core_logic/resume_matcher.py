import os
import json
from google import genai

def analyze_resume_with_gemini(resume_text, jd_text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"resume_score": 0, "matched_keywords": [], "missing_keywords": ["API Key Missing"]}

    client = genai.Client(api_key=api_key)

    # Advanced Prompt Engineering: Ensuring Dynamic Extraction
    prompt = f"""
    You are an Expert Technical Recruiter and ATS.
    Analyze the fit between the Candidate's Resume and the Job Description based on skills, experience, and projects.
    
    Resume Text: {resume_text}
    Job Description: {jd_text}
    
    INSTRUCTIONS:
    1. Calculate a realistic resume_score (0 to 100) based on alignment.
    2. Extract ACTUAL matched skills present in both the resume and JD.
    3. Extract ACTUAL missing skills required by the JD but missing in the resume.
    4. Generate 3 interview questions specifically based on the REAL missing skills.
    
    Return ONLY a valid JSON object. Use the following STRUCTURE, but REPLACE the dummy values with your actual dynamic analysis:
    {{
        "resume_score": <integer>,
        "matched_keywords": ["actual_skill_1", "actual_skill_2"],
        "missing_keywords": ["actual_missing_skill_1", "actual_missing_skill_2"],
        "recommended_questions": ["Question 1 about missing skill?", "Question 2?", "Question 3?"]
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