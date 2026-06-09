# AI Interview Insight 🧠⚡

**Advanced Multimodal Assessment Platform for Engineers**

AI Interview Insight is a next-generation HR-tech application designed to automate and enhance the technical recruitment process. By leveraging Multimodal Large Language Models (LLMs), it concurrently analyzes a candidate's video interview, parses their resume, and cross-references it with a target Job Description (JD) to generate a comprehensive, bias-free hiring verdict.

<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/deede475-ce7f-4213-92a3-2b3dd601d28d" />


---

## ✨ Key Features

* **🎥 Multimodal Video Analysis:** Processes interview video and audio to evaluate technical accuracy, communication skills, and articulation using the Gemini 2.5 Flash API.
* **📄 Semantic Resume Matching:** Parses PDF resumes and dynamically extracts actual matched and missing technical skills compared to the JD.
* **❓ Dynamic Interview Questions:** Automatically generates context-aware follow-up interview questions tailored to the candidate's specific "missing skills".
* **🛡️ Smart Fallback Logic:** Engineered with a robust, dynamic text-based fallback mechanism to ensure the system never crashes during API timeouts or rate limits.
* **📊 Calibrated Scoring System:** Calculates a weighted overall score (Resume + Technical + Communication) to provide a definitive hiring verdict (e.g., "Strong Hire 🌟", "Reject ❌").
* **✨ Modern Glassmorphism UI:** Features an interactive, highly responsive, and accessible frontend built without heavy frontend frameworks.

---

## 🛠️ Tech Stack

**Frontend:**
* HTML5, CSS3 (Custom Glassmorphism UI)
* Vanilla JavaScript (Real-time DOM manipulation & animations)

**Backend:**
* Python 3
* Flask (Web Framework)
* PyPDF2 (Document Parsing)
* Gunicorn (Production WSGI Server)

**Artificial Intelligence:**
* Google GenAI API (Gemini 2.5 Flash Multimodal)
* Prompt Engineering & JSON Schema structuring

---

## 🚀 Installation & Local Setup

**1. Clone the repository**
```bash
git clone [https://github.com/the-miz4u/ai-interview-insight.git](https://github.com/the-miz4u/ai-interview-insight.git)
cd ai-interview-insight
```

2. Create and activate a virtual environment
   Bash
  python -m venv venv  
  # On Windows:
  venv\Scripts\activate
  # On Mac/Linux:
  source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

5. Set up Environment Variables
   Create a .env file in the root directory and add your Google Gemini API key:
   GEMINI_API_KEY=your_actual_api_key_here

6. Run the application
   python app.py
   Navigate to http://127.0.0.1:5000 in your web browser.

---

## ☁️ Cloud Deployment (Production Ready)

This application is fully optimized for seamless deployment on modern cloud hosting platforms like **Render**, **Heroku**, or **AWS**. 

**Standard WSGI Configuration:**
* 🛠️ **Build Command:** `pip install -r requirements.txt`
* 🚀 **Start Command:** `gunicorn app:app`

> **Note:** Ensure that your `GEMINI_API_KEY` is securely added to the Environment Variables/Secrets of your chosen hosting provider before initiating the deploy.

---
---

## ☁️ Cloud Deployment (Production Ready)

This application is fully optimized for seamless deployment on modern cloud hosting platforms like **Render**, **Heroku**, or **AWS**. 

**Standard WSGI Configuration:**
* 🛠️ **Build Command:** `pip install -r requirements.txt`
* 🚀 **Start Command:** `gunicorn app:app`

> **Note:** Ensure that your `GEMINI_API_KEY` is securely added to the Environment Variables/Secrets of your chosen hosting provider before initiating the deploy.

---

## 👨‍💻 Developed By

**Manish Sharma** 🎓 *B.Tech Computer Science & Engineering | University of Engineering and Management (UEM), Jaipur*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/manish-sharma-0000172a0)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/the-miz-4u)

*If you found this project helpful or insightful, don't forget to leave a ⭐ on the repository!*
