import os
import fitz
import groq
from flask import Flask, render_template, request, jsonify, send_file
from fpdf import FPDF

def save_as_pdf(text, filename):
    """Saves text as a formatted PDF with basic font support."""
    try:
        # Create PDF with default fonts
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Handle special characters
        def clean_text(text):
            # Replace problematic characters with ASCII equivalents
            replacements = {
                '–': '-',    # en dash
                '—': '-',    # em dash
                '"': '"',    # smart quotes
                '"': '"',
                ''': "'",    # smart apostrophes
                ''': "'",
                '•': '*',    # bullet points
                '…': '...',  # ellipsis
                '\u2013': '-',  # additional en dash
                '\u2014': '-',  # additional em dash
                '\u2018': "'",  # additional smart quotes
                '\u2019': "'",
                '\u201C': '"',
                '\u201D': '"',
                '\u2022': '*',  # additional bullet point
                '\u2026': '...' # additional ellipsis
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text
        
        # Clean and encode text
        cleaned_text = clean_text(text)
        
        # Write text in chunks to handle long content
        pdf.multi_cell(0, 10, cleaned_text)
        
        pdf_path = os.path.join(OUTPUT_FOLDER, filename)
        pdf.output(pdf_path)
        return pdf_path
    
    except Exception as e:
        print(f"PDF Creation Error: {str(e)}")
        raise

app = Flask(__name__)

# Set upload and output folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "enhanced_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "Your GROK API key here.")
client = groq.Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
        return text.strip() if text.strip() else "Error: No text extracted from the resume."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def enhance_resume_with_ai(text):
    """Enhances resume text using Groq API."""
    try:
        prompt = """Please enhance this resume while:
        1. Maintaining all original information
        2. Improving the formatting and structure
        3. Using more impactful action verbs
        4. Quantifying achievements where possible
        5. Keeping the original sections
        6. Preserving dates and contact information
        
        Ensure the enhancement is professional and truthful."""
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a professional resume enhancer focusing on clarity, impact, and truthfulness."},
                {"role": "user", "content": f"{prompt}\n\nOriginal Resume:\n{text}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip() if response.choices else "Error: No valid AI response."
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_skills_and_recommend_courses(resume_text, job_description):
    """Analyzes skills gap and recommends relevant courses."""
    try:
        prompt = """Analyze the resume against the job description and provide:
        1. Skills match analysis (percentage match for key requirements)
        2. Missing skills and areas for improvement
        3. Specific course recommendations from Udemy, Coursera, or similar platforms
        4. Additional suggestions for skill development
        
        Format the response in clear sections with bullet points."""
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a career advisor specializing in skill gap analysis and learning recommendations."},
                {"role": "user", "content": f"{prompt}\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip() if response.choices else "Error: No valid AI response."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("Resumizer.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    """Handles PDF upload and enhancement."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Invalid file format. Only PDF is allowed."}), 400
    
    try:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        
        extracted_text = extract_text_from_pdf(file_path)
        if "Error" in extracted_text:
            return jsonify({"error": extracted_text}), 500
        
        enhanced_text = enhance_resume_with_ai(extracted_text)
        if "Error" in enhanced_text:
            return jsonify({"error": enhanced_text}), 500
        
        pdf_filename = f"enhanced_{file.filename}"
        pdf_path = save_as_pdf(enhanced_text, pdf_filename)
        
        return jsonify({
            "enhanced_resume": enhanced_text,
            "download_url": f"/download/{pdf_filename}",
            "original_text": extracted_text
        })
    
    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

@app.route("/analyze_job_match", methods=["POST"])
def analyze_job_match():
    """Analyzes resume against job description and recommends courses."""
    try:
        data = request.get_json()
        job_description = data.get("job_description", "")
        resume_text = data.get("resume_text", "")
        
        if not job_description or not resume_text:
            return jsonify({"error": "Both resume and job description are required"}), 400
        
        analysis = analyze_skills_and_recommend_courses(resume_text, job_description)
        return jsonify({"analysis": analysis})
    
    except Exception as e:
        return jsonify({"error": f"Analysis error: {str(e)}"}), 500

@app.route("/download/<filename>")
def download_file(filename):
    """Downloads enhanced resume PDF.""" 
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, as_attachment=True) if os.path.exists(file_path) else (jsonify({"error": "File not found"}), 404)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
