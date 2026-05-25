from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

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
        # Frontend se data receive karna
        jd_text = request.form.get('jd')
        resume_file = request.files.get('resume')

        if not resume_file or not jd_text:
            return jsonify({"status": "error", "message": "Please upload a Resume and enter a Job Description."})

        # File ko temporarily save karna evaluation ke liye
        filepath = os.path.join("datasets", resume_file.filename)
        resume_file.save(filepath)

        # AI Function Call karna
        nlp_result = evaluate_resume(filepath, jd_text)

        # Temp file delete karna taaki memory full na ho
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "status": "success",
            "message": "Resume Evaluated Successfully!",
            "resume_score": nlp_result["score"],
            "matched_keywords": nlp_result["matched_keywords"],
            "missing_keywords": nlp_result["missing_keywords"]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # debug=True rakhne se server auto-reload hoga jab aap code change karenge
    app.run(debug=True, port=5000)