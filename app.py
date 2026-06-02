from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
from dotenv import load_dotenv

# Apne core logics import karein
from core_logic.video_analyzer import analyze_interview
from core_logic.resume_matcher import analyze_resume_with_gemini

# Environment variables load karein
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Helper function: PDF se text nikalne ke liye
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + " "
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text

@app.route('/evaluate', methods=['POST'])
def evaluate_candidate():
    try:
        jd_text = request.form.get('jd')
        resume_file = request.files.get('resume')
        video_file = request.files.get('video')

        if not resume_file or not jd_text or not video_file:
            return jsonify({"status": "error", "message": "Please upload Resume, Video and enter JD."})

        # Save files temporarily (Safe folder creation)
        os.makedirs("datasets", exist_ok=True)
        resume_path = os.path.join("datasets", resume_file.filename)
        video_path = os.path.join("datasets", video_file.filename)
        
        resume_file.save(resume_path)
        video_file.save(video_path)

        # 1. Resume (PDF) se text extract karo
        print("[INFO] Extracting text from Resume...")
        resume_text = extract_text_from_pdf(resume_path)

        # 2. Evaluate Resume (Naya Gemini LLM Logic)
        nlp_result = analyze_resume_with_gemini(resume_text, jd_text)

        # 3. Evaluate Video & Audio (Gemini Multimodal AI)
        video_result = analyze_interview(video_path, jd_text)

        # Cleanup temp files
        if os.path.exists(resume_path): os.remove(resume_path)
        if os.path.exists(video_path): os.remove(video_path)

        if "error" in video_result:
            return jsonify({"status": "error", "message": video_result["error"]})

        # --- NAYA LOGIC: Hiring Recommendation ---
        res_score = nlp_result.get("resume_score", 0)
        tech_score = video_result.get("technical_score", 0)
        conf_score = video_result.get("confidence_score", 0)
        
        # Weighted Average
        total_score = (res_score * 0.3) + (tech_score * 0.5) + (conf_score * 0.2)
        
        if total_score >= 80:
            hiring_status = "Strong Hire 🌟"
            status_color = "#4ade80"
        elif total_score >= 65:
            hiring_status = "Hire ✅"
            status_color = "#3b82f6"
        elif total_score >= 50:
            hiring_status = "Maybe / Needs Review ⚠️"
            status_color = "#fbbf24"
        else:
            hiring_status = "Reject ❌"
            status_color = "#f87171"

        # Send final combined report
        return jsonify({
            "status": "success",
            "message": "Evaluation Complete!",
            "resume_score": res_score,
            "matched_keywords": nlp_result.get("matched_keywords", []),
            "missing_keywords": nlp_result.get("missing_keywords", []),
            "recommended_questions": nlp_result.get("recommended_questions", []),
            "technical_score": tech_score,
            "confidence_score": conf_score,
            "video_feedback": video_result.get("feedback", "No feedback generated."),
            "hiring_status": hiring_status,
            "status_color": status_color
        })

    except Exception as e:
        import traceback
        print("[CRITICAL ERROR IN APP.PY]")
        traceback.print_exc() # Terminal me exact error batayega
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)