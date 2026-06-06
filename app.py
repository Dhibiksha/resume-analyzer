from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    if not file.filename.lower().endswith(".pdf"):
        return "Please upload a PDF file only."
    
    if file:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        try:
            reader = PdfReader(filepath)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        except Exception as e:
            return f"Error reading PDF: {str(e)}"

        skills = [
            "Python",
            "Java",
            "C",
            "C++",
            "HTML",
            "CSS",
            "JavaScript",
            "MySQL",
            "AWS",
            "Azure",
            "Git"
        ]

        detected = []

        for skill in skills:
            if skill.lower() in text.lower():
                detected.append(skill)

        score = len(detected) * 10

        if score > 100:
            score = 100
        
        role = "General"

        if "AWS" in detected or "Azure" in detected:
            role = "Cloud Engineer"
        elif "Python" in detected:
            role = "Python Developer"
        elif "HTML" in detected and "CSS" in detected:
            role = "Frontend Developer"
        elif "MySQL" in detected:
            role = "Database Developer"

        return f"""
<!DOCTYPE html>
<html>
<head>
<title>Analysis Result</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background-color: #f4f7fc;
    margin: 0;
    padding: 30px;
}}

.container {{
    max-width: 900px;
    margin: auto;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.score {{
    font-size: 32px;
    font-weight: bold;
    color: #2563eb;
}}

.skill {{
    display: inline-block;
    background: #2563eb;
    color: white;
    padding: 8px 15px;
    margin: 5px;
    border-radius: 20px;
}}

.resume-text {{
    max-height: 300px;
    overflow-y: auto;
    background: #f8f8f8;
    padding: 15px;
    border-radius: 10px;
}}

</style>
</head>

<body>

<div class="container">

    <div class="card">
        <h1>Resume Analysis Result</h1>
    </div>

    <div class="card">
        <h2>Resume Score</h2>
        <div class="score">{score}/100</div>
    </div>

    <div class="card">
        <h2>Recommended Role</h2>
        <h3>{role}</h3>
    </div>

    <div class="card">
        <h2>Detected Skills</h2>
        {''.join(f'<span class="skill">{skill}</span>' for skill in detected)}
    </div>

    <div class="card">
        <h2>Resume Content</h2>
        <div class="resume-text">
            <pre>{text}</pre>
        </div>
    </div>

</div>

</body>
</html>
"""

    return "No file uploaded"


if __name__ == "__main__":
    app.run(debug=True)