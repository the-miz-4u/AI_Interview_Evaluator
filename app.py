from flask import Flask, render_template, request, jsonify
import os
import PyPDF2  # <-- PDF se text nikalne ke liye
from dotenv import load_dotenv

# Apne dono core logics import karein
from core_logic.video_analyzer import analyze_interview
from core_logic.resume_matcher import analyze_resume_with_gemini

# Load environment variables (API Keys)
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Helper function: PDF file padhkar usme se text nikalne ke liye
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + " "
    except Exception as e:
        print("PDF extraction error:", e)
    return text

@app.route('/evaluate', methods=['POST'])
def evaluate_candidate():
    try:
        jd_text = request.form.get('jd')
        resume_file = request.files.get('resume')
        video_file = request.files.get('video')

        if not resume_file or not jd_text or not video_file:
            return jsonify({"status": "error", "message": "Please upload Resume, Video and enter JD."})

        # Save files temporarily
        resume_path = os.path.join("datasets", resume_file.filename)
        video_path = os.path.join("datasets", video_file.filename)
        resume_file.save(resume_path)
        video_file.save(video_path)

        # 1. NAYA STEP: Resume (PDF) se text extract karo
        print("Extracting text from Resume...")
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

        # (Iske upar video_result aur cleanup ka code hai)

        if "error" in video_result:
            return jsonify({"status": "error", "message": video_result["error"]})

        # --- NAYA LOGIC: Hiring Recommendation ---
        res_score = nlp_result.get("resume_score", 0)
        tech_score = video_result.get("technical_score", 0)
        conf_score = video_result.get("confidence_score", 0)
        
        # Weighted Average (Tech ko zyada weightage)
        total_score = (res_score * 0.3) + (tech_score * 0.5) + (conf_score * 0.2)
        
        if total_score >= 80:
            hiring_status = "Strong Hire 🌟"
            status_color = "#4ade80" # Green
        elif total_score >= 65:
            hiring_status = "Hire ✅"
            status_color = "#3b82f6" # Blue
        elif total_score >= 50:
            hiring_status = "Maybe / Needs Review ⚠️"
            status_color = "#fbbf24" # Yellow
        else:
            hiring_status = "Reject ❌"
            status_color = "#f87171" # Red

        # Send final combined report
        return jsonify({
            "status": "success",
            "message": "Evaluation Complete!",
            "resume_score": res_score,
            "matched_keywords": nlp_result.get("matched_keywords", []),
            "missing_keywords": nlp_result.get("missing_keywords", []),
            "recommended_questions": nlp_result.get("recommended_questions", ["No questions generated."]),
            "technical_score": tech_score,
            "confidence_score": conf_score,
            "video_feedback": video_result.get("feedback", "No feedback generated."),
            "hiring_status": hiring_status,
            "status_color": status_color
        })
        # Send final combined report (Nayi keys ke sath update kiya gaya hai)
        return jsonify({
            "status": "success",
            "message": "Evaluation Complete!",
            "resume_score": nlp_result.get("resume_score", 0),
            "matched_keywords": nlp_result.get("matched_keywords", []),
            "missing_keywords": nlp_result.get("missing_keywords", []),
            "technical_score": video_result.get("technical_score", 0),
            "confidence_score": video_result.get("confidence_score", 0),
            "video_feedback": video_result.get("feedback", "No feedback generated.")
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # debug=True rakhne se server auto-reload hoga jab aap code change karenge
    app.run(debug=True, port=5000)