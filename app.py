from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from core_logic.video_analyzer import analyze_interview

# Load environment variables (API Keys)
load_dotenv()

app = Flask(__name__)

# Basic route to load the homepage
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint jahan UI se data aayega (abhi iska skeleton bana rahe hain)
from core_logic.resume_matcher import evaluate_resume

@app.route('/evaluate', methods=['POST'])
def evaluate_candidate():
    try:
        jd_text = request.form.get('jd')
        resume_file = request.files.get('resume')
        video_file = request.files.get('video') # Video file from frontend

        if not resume_file or not jd_text or not video_file:
            return jsonify({"status": "error", "message": "Please upload Resume, Video and enter JD."})

        # Save files temporarily
        resume_path = os.path.join("datasets", resume_file.filename)
        video_path = os.path.join("datasets", video_file.filename)
        resume_file.save(resume_path)
        video_file.save(video_path)

        # 1. Evaluate Resume (TF-IDF NLP)
        nlp_result = evaluate_resume(resume_path, jd_text)

        # 2. Evaluate Video & Audio (Gemini Multimodal AI)
        video_result = analyze_interview(video_path, jd_text)

        # Cleanup temp files
        if os.path.exists(resume_path): os.remove(resume_path)
        if os.path.exists(video_path): os.remove(video_path)

        if "error" in video_result:
            return jsonify({"status": "error", "message": video_result["error"]})

        # Send final combined report
        return jsonify({
            "status": "success",
            "message": "Evaluation Complete!",
            "resume_score": nlp_result["score"],
            "matched_keywords": nlp_result["matched_keywords"],
            "missing_keywords": nlp_result["missing_keywords"],
            "technical_score": video_result.get("technical_score", 0),
            "confidence_score": video_result.get("confidence_score", 0),
            "video_feedback": video_result.get("feedback", "No feedback generated.")
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
if __name__ == '__main__':
    # debug=True rakhne se server auto-reload hoga jab aap code change karenge
    app.run(debug=True, port=5000)