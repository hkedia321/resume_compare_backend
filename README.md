Resume Matcher Backend
======================

This is a Python backend for a Resume Review and Job Matching project. It provides an API to parse resumes (PDF), extract job descriptions from URLs, and compare them using advanced AI models to provide actionable feedback and a match score.

---

Tech Stack
----------
- **Python 3.9+**
- **FastAPI**: For building the REST API
- **LangChain**: For orchestrating LLM chains and prompts
- **OpenAI (ChatGPT)**: For resume parsing, job extraction, and comparison logic
- **PyPDF2**: For extracting text from PDF resumes
- **BeautifulSoup4 & Requests**: For scraping and parsing job descriptions from web pages
- **Uvicorn**: For running the FastAPI server
- **python-dotenv**: For environment variable management

---

Built using ChatGPT and Cursor
-----------------------------
This project was developed with the help of OpenAI's ChatGPT and the Cursor editor, enabling rapid prototyping and AI-powered code generation.

---

Features
--------
- **/compare-resume-job/**: Upload a PDF resume and provide a job URL to receive a structured comparison, match score, and improvement suggestions.
- **Resume Parsing**: Extracts structured data (skills, experience, education, etc.) from PDF resumes using LLMs.
- **Job Parsing**: Extracts structured job requirements from job posting URLs.
- **AI-Powered Comparison**: Uses LLMs to compare resume and job, returning a match score and actionable feedback.

---

Setup Instructions
------------------
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

---

License
-------
This project is for educational and demonstration purposes only. 