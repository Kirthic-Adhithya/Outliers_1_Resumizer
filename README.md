# Resumizer

An AI-powered web application that enhances resumes by restructuring, optimizing keywords, and generating job-tailored resumes.  
Built with Flask (Python backend), HTML/CSS/JS (frontend), and integrated PDF processing.

---

## Features
- Upload Resume – Supports PDF uploads.  
- AI-Powered Enhancement – Improves formatting, structure, and relevance.  
- Keyword Optimization – Adds job-relevant keywords to improve ATS (Applicant Tracking System) scores.  
- Enhanced Resume Output – Download optimized resumes in PDF format.  
- Clean Frontend – Simple UI with HTML, CSS, and JavaScript.  

---

## Tech Stack
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, Flask  
**AI/Processing:** Custom text enhancement (`text_groq.py`)  
**File Handling:** PyPDF2 / FPDF (depending on enhancement logic)  
**Storage:** Local uploads + enhanced resume storage  

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Outliers-Resumizer.git
cd Outliers-Resumizer
```
### 2. Create Virtual Environment & Install Dependencies
```bash
  python -m venv venv
  source venv/bin/activate   # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
```
### 3. Run the App
```bash
python app.py
```
The app will be live at http://127.0.0.1:5000/

### Project Structure
    Outliers_Resumizer/
    │── app.py                 # Flask backend
    │── text_groq.py           # Resume enhancement logic
    │── README.md              # Project documentation
    │
    ├── templates/
    │   └── Resumizer.html     # Frontend (HTML template)
    │
    ├── static/
    │   ├── Resumizer.css      # Stylesheet
    │   └── resumizer.js       # JavaScript for UI
    │
    ├── uploads/               # Uploaded resumes
    ├── enhanced_resumes/      # AI-enhanced resumes
    └── requirements.txt       # Python dependencies
---
### Future Improvements

- Upload Job Description (JD) and tailor resume accordingly.

- Store resume history in a database (SQLite/Postgres).

- Deploy on Render / Heroku / Vercel.

- Add analytics – compare keyword matches before vs after enhancement.

- Improve UI with drag-and-drop upload & progress bar.
