# from flask import Flask, request, jsonify, send_from_directory
# from werkzeug.utils import secure_filename
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import PyPDF2
# import io
# from PIL import Image
# import pytesseract
# import os

# # Create the Flask app
# app = Flask(__name__, static_folder=r'C:\\Users\\user\\OneDrive\\Desktop\\PROJECT\\static')

# # Define sample job descriptions with required skills
# job_descriptions = {
#     'data_scientist': "Must have experience with Python, machine learning, and data analysis.",
#     'software_engineer': "Proficiency in Java, algorithms, and software design is required.",
#     'administrative_assistant': "Experience with Excel, PowerPoint, CRM, problem-solving, and team leadership."
# }

# # Define required skills for each job
# required_skills = {
#     'data_scientist': ['python', 'machine learning', 'data analysis'],
#     'software_engineer': ['java', 'algorithms', 'software design'],
#     'administrative_assistant': ['excel', 'powerpoint', 'crm', 'problem-solving', 'team leadership']
# }

# # Initialize vectorizer and transform job descriptions
# vectorizer = TfidfVectorizer()
# job_description_vectors = vectorizer.fit_transform(job_descriptions.values())

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     try:
#         pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(pdf_file))
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ""

# # Function to extract text from JPG
# def extract_text_from_jpg(jpg_file):
#     try:
#         image = Image.open(io.BytesIO(jpg_file))
#         text = pytesseract.image_to_string(image)
#         return text
#     except Exception as e:
#         print(f"Error extracting text from JPG: {e}")
#         return ""

# # Function to extract skills from resume text
# def extract_skills(resume_text, job_title):
#     skills = required_skills.get(job_title.lower(), [])
#     resume_text_lower = resume_text.lower()
#     score = sum(1 for skill in skills if skill in resume_text_lower)
#     return score, len(skills)

# @app.route('/')
# def index():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/add_resume')
# def add_resume():
#     return send_from_directory(app.static_folder, 'add_resume.html')
# @app.route('/help_and_support')
# def help_and_support():
#     return send_from_directory(app.static_folder, 'help_and_support.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         if 'resume' not in request.files or 'job' not in request.form:
#             return jsonify({"error": "No file part or job title missing"}), 400

#         file = request.files['resume']
#         job_title = request.form['job'].strip().lower()

#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400

#         file_extension = file.filename.rsplit('.', 1)[1].lower()
        
#         if file and file_extension in ['pdf', 'jpg', 'jpeg']:
#             if file_extension in ['pdf']:
#                 resume_text = extract_text_from_pdf(file.read())
#             elif file_extension in ['jpg', 'jpeg']:
#                 resume_text = extract_text_from_jpg(file.read())
            
#             if not resume_text:
#                 return jsonify({"error": "Unable to extract text from file"}), 500
            
#             # Extract skills and calculate score
#             skills_count, total_skills = extract_skills(resume_text, job_title)
#             ats_score = (skills_count / total_skills) * 100 if total_skills > 0 else 0

#             return jsonify({"score": ats_score}), 200

#         return jsonify({"error": "Invalid file format"}), 400
#     except Exception as e:
#         print(f"Error during upload: {e}")
#         return jsonify({"error": "An error occurred while uploading the file"}), 500

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2
import io
from PIL import Image
import pytesseract
import os

# Create the Flask app
app = Flask(__name__, static_folder=r'C:\\Users\\user\\OneDrive\\Desktop\\PROJECT\\static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Define sample job descriptions with required skills
job_descriptions = {
    'data_scientist': "Must have experience with Python, machine learning, and data analysis.",
    'software_engineer': "Proficiency in Java, algorithms, and software design is required.",
    'administrative_assistant': "Experience with Excel, PowerPoint, CRM, problem-solving, and team leadership.",
    'project_manager': "Experience with resource coordination, process improvement, strategic planning, people management, cross-functional leadership"
}

# Define required skills for each job
required_skills = {
    'data_scientist': ['python', 'machine learning', 'data analysis'],
    'software_engineer': ['java', 'algorithms', 'software design'],
    'administrative_assistant': ['excel', 'powerpoint', 'crm', 'problem-solving', 'team leadership'],
    'project_manager': ["process improvement", "strategic planning", "people management", "cross-functional leadership"]
}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Function to extract text from JPG
def extract_text_from_jpg(jpg_file):
    try:
        image = Image.open(io.BytesIO(jpg_file))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from JPG: {e}")
        return ""

# Function to extract skills from resume text
def extract_skills(resume_text, job_title):
    skills = required_skills.get(job_title.lower(), [])
    resume_text_lower = resume_text.lower()
    matched_skills = [skill for skill in skills if skill in resume_text_lower]
    unmatched_skills = [skill for skill in skills if skill not in matched_skills]
    return len(matched_skills), len(skills), matched_skills, unmatched_skills

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/add_resume')
def add_resume():
    return send_from_directory(app.static_folder, 'add_resume.html')

@app.route('/help_and_support')
def help_and_support():
    return send_from_directory(app.static_folder, 'help_and_support.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'resume' not in request.files or 'job' not in request.form:
            return jsonify({"error": "No file part or job title missing"}), 400

        file = request.files['resume']
        job_title = request.form['job'].strip().lower()

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_extension = file.filename.rsplit('.', 1)[1].lower()
        
        if file and file_extension in ['pdf', 'jpg', 'jpeg']:
            if file_extension == 'pdf':
                resume_text = extract_text_from_pdf(file.read())
            elif file_extension in ['jpg', 'jpeg']:
                resume_text = extract_text_from_jpg(file.read())
            
            if not resume_text:
                return jsonify({"error": "Unable to extract text from file"}), 500
            
            skills_count, total_skills, matched_skills, unmatched_skills = extract_skills(resume_text, job_title)
            print(f"Skills Count: {skills_count}, Total Skills: {total_skills}, Matched Skills: {matched_skills}, Unmatched Skills: {unmatched_skills}")
            
            ats_score = (skills_count / total_skills) * 100 if total_skills > 0 else 0
            print(f"ATS Score: {ats_score}")
            
            return jsonify({"score": ats_score, "matched_skills": matched_skills, "unmatched_skills": unmatched_skills}), 200

        return jsonify({"error": "Invalid file format"}), 400
    except Exception as e:
        print(f"Error during upload: {e}")
        return jsonify({"error": "An error occurred while uploading the file"}), 500

if __name__ == '__main__':
    app.run(debug=True)

