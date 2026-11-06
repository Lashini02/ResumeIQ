# ResumeIQ – Resume & Job Match Analyzer

**Developed by Lashini Chamodi**

ResumeIQ is a web-based resume analysis tool that helps job seekers understand how well their resume matches a particular job description.

Users can upload their resume in PDF format, paste a job description, and receive an analysis showing a job match score, matched skills, missing skills, relevant keywords, and suggestions for improvement.

The main purpose of this project is to help job seekers identify areas where their resumes can be improved before applying for jobs.

---

## Project Overview

Finding a suitable job is not only about having the right qualifications. It is also important to present relevant skills and experience clearly in a resume.

ResumeIQ aims to make this process easier by comparing the content of a resume with a given job description.

The application uses Python-based text processing techniques and Natural Language Processing (NLP) methods to analyze resume content and identify relevant information.

## Key Features

### 1. Resume Upload
- Upload resumes in PDF format.
- Extract text from uploaded PDF files.
- Validate file type and file size.
- Support PDF files up to 5 MB.

### 2. Job Description Analysis
- Paste a job description into the application.
- Extract important skills and keywords.
- Identify relevant requirements from the job description.

### 3. Resume and Job Matching
- Calculate an estimated job match score.
- Compare resume skills with job requirements.
- Identify matched skills.
- Highlight missing skills.
- Calculate text similarity using TF-IDF and Cosine Similarity.

### 4. Resume Section Detection
Identify important resume sections, including:

- Professional Summary
- Technical Skills
- Work Experience
- Education
- Projects
- Certifications
- Achievements
- Additional Information

The application also checks for contact details such as email, phone number, LinkedIn, and GitHub.

### 5. Improvement Suggestions
- Provide suggestions based on the analysis.
- Highlight missing skills and keywords.
- Help users identify areas that may need improvement.

### 6. PDF Analysis Report
- Generate a downloadable PDF report.
- Include the match score and text similarity.
- Display matched and missing skills.
- Include keyword analysis, resume sections, and improvement suggestions.

### 7. User-Friendly Interface
- Simple and clean interface.
- Responsive layout for different screen sizes.
- Easy-to-understand analysis results.
- Compact result sections to make important information easier to find.

---

## Technologies Used

### Frontend
- React.js
- Vite
- JavaScript
- HTML5
- CSS3
- Lucide React (Icons)

### Backend
- Python
- Flask
- Flask-CORS

### NLP and Text Processing
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- Rule-based Skill Extraction

### PDF Processing and Reporting
- PyMuPDF (PDF text extraction)
- ReportLab (PDF report generation)

### Development Tools
- Visual Studio Code
- Git
- GitHub
- npm

---

## How It Works

The application follows a simple process:

1. The user uploads a resume in PDF format.
2. The backend extracts text from the uploaded resume using PyMuPDF.
3. The user provides a job description.
4. The NLP analyzer identifies skills and keywords from both documents.
5. The system compares the resume content with the job requirements.
6. A match score is calculated using skill matching and text similarity.
7. The application displays the analysis results.
8. The user can download a PDF report containing the results.

---

## Project Structure

```text
ResumeIQ/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
├── backend/
│   ├── app.py
│   ├── section_detector.py
│   ├── nlp_analyzer.py
│   ├── report_generator.py
│   ├── requirements.txt
│   └── venv/
│
└── README.md
```

### Main Backend Files

| File | Description |
|---|---|
| `app.py` | Handles API requests, PDF uploads, and communication with the frontend. |
| `section_detector.py` | Identifies important resume sections and contact information. |
| `nlp_analyzer.py` | Extracts skills and keywords and calculates the job match score. |
| `report_generator.py` | Generates downloadable PDF analysis reports. |
| `requirements.txt` | Contains the Python dependencies required for the backend. |

---

## Installation and Setup

Follow these steps to run ResumeIQ on your local machine.

### Prerequisites

Make sure you have installed:

- Python 3.10 or later
- Node.js and npm
- Visual Studio Code
- Git

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd ResumeIQ
```

### 2. Set Up the Backend

Open a terminal and navigate to the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask backend:

```bash
python app.py
```

The backend should run at:

`http://127.0.0.1:5000`

### 3. Set Up the Frontend

Open a separate terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install the required packages:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Open the application in your browser:

`http://localhost:5173`

**Note:** Keep both the frontend and backend terminals running while using the application.

---

## API Endpoints

The Flask backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Checks whether the backend is running. |
| POST | `/api/analyze` | Analyzes the uploaded resume against a job description. |
| POST | `/api/report` | Generates a downloadable PDF analysis report. |

### Health Check

```http
GET /api/health
```

This endpoint checks the backend server status.

### Resume Analysis

```http
POST /api/analyze
```

Accepts:
- `resume` – PDF resume file.
- `job_description` – Job description text.

### PDF Report Generation

```http
POST /api/report
```

Accepts the same resume and job description inputs and returns a PDF report.

---

## Current Analysis Approach

ResumeIQ uses a combination of rule-based skill matching and text similarity techniques.

**Skill Matching:** The system uses predefined skill names and aliases to identify relevant skills in the resume and job description.

**TF-IDF:** TF-IDF (Term Frequency–Inverse Document Frequency) helps identify important words and phrases in the text.

**Cosine Similarity:** Cosine Similarity is used to estimate how similar the resume text is to the job description.

The match score combines skill coverage and text similarity when job skills are detected.

The result is an estimated match score, not an official ATS score or a guarantee of selection by an employer.

---

## Future Improvements

Some features that could be added in future versions include:

- Integration with advanced AI and NLP models.
- More accurate context-based skill identification.
- Support for additional resume formats such as DOCX.
- Resume formatting and readability analysis.
- More detailed recommendations based on job roles.
- User accounts and analysis history.
- Resume improvement and keyword recommendation features.
- Automated resume comparison for multiple job opportunities.
- Cloud deployment.

---

## Learning Outcomes

Through this project, I aim to improve my practical knowledge and gain experience in:

- Building frontend applications using React.
- Developing REST APIs using Python Flask.
- Working with PDF text extraction.
- Applying NLP and text similarity techniques.
- Connecting frontend and backend applications.
- Handling file uploads and API requests.
- Generating downloadable PDF reports.
- Managing and documenting a software development project using Git and GitHub.

---

## Disclaimer

ResumeIQ is an educational and portfolio project designed to assist with resume analysis.

Its results are based on predefined skill matching and text similarity techniques. The match score should be treated as an estimate rather than an official ATS evaluation or a prediction of recruitment success.

---

## Author

**Lashini Chamodi**

IT Undergraduate | Networking and Mobile Computing

Interested in Business Analysis, Project Management, Software Quality Assurance, Web Development, and Cybersecurity.

- GitHub: [Lashini02](https://github.com/Lashini02)

---

*ResumeIQ © 2026 · Built with React & Python · Developed by Lashini Chamodi*
