import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    """PDF file se raw text nikalne ka function"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + " "
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def clean_text(text):
    """Text me se faltu characters hatane ke liye"""
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

def get_keywords(text):
    """Advanced keyword extraction: Stop words aur generic words ko ignore karna"""
    custom_stop_words = {'skills', 'looking', 'developer', 'experience', 'required', 'years', 'work', 'good', 'knowledge', 'candidate', 'role', 'with', 'this'}
    all_stop_words = ENGLISH_STOP_WORDS.union(custom_stop_words)
    
    words = set(clean_text(text).split())
    filtered_keywords = {w for w in words if len(w) > 3 and w not in all_stop_words}
    return filtered_keywords

def evaluate_resume(pdf_path, jd_text):
    """Main function jo Resume aur JD ko compare karega"""
    if not jd_text:
        return {"score": 0, "matched_keywords": [], "missing_keywords": []}

    # 1. Extract and Clean Text
    resume_text = extract_text_from_pdf(pdf_path)
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)

    if not clean_resume:
         return {"error": "Could not extract text from Resume."}

    # 2. NLP Logic: TF-IDF & Cosine Similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([clean_resume, clean_jd])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)

    # 3. Explainable AI: Proof ke liye keywords nikalna
    resume_keywords = get_keywords(resume_text)
    jd_keywords = get_keywords(jd_text)

    matched = list(jd_keywords.intersection(resume_keywords))
    missing = list(jd_keywords.difference(resume_keywords))

    return {
        "score": score,
        "matched_keywords": matched[:10], 
        "missing_keywords": missing[:10]
    }