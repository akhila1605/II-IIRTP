from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Make sure uploads folder exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    job_role = request.form['job_role']
    file = request.files['resume']

    if file.filename == '':
        return "No file uploaded"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Read resume text
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        resume_text = f.read().lower()

    # 🔹 RESULT LOGIC
    result = "Selected"
    suggestions = []

    # 🔴 Checking conditions
    if job_role.lower() not in resume_text:
        result = "Rejected"
        suggestions.append(f"Add keywords related to {job_role}")

    if "skills" not in resume_text:
        result = "Rejected"
        suggestions.append("Add a Skills section")

    if "project" not in resume_text:
        result = "Rejected"
        suggestions.append("Include your Projects")

    if "experience" not in resume_text:
        suggestions.append("Mention work experience (if any)")

    if "education" not in resume_text:
        suggestions.append("Add Education details")

    # 🔴 IMPORTANT: Prevent empty suggestions
    if not suggestions:
        suggestions.append("Your resume looks good. Improve formatting and add more keywords.")

    print("Result:", result)
    print("Suggestions:", suggestions)

    return render_template('result.html', result=result, suggestions=suggestions)


if __name__ == '__main__':
    app.run(debug=True)