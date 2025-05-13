from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.resume_agent import parse_resume
from agents.job_agent import parse_job_link
from agents.compare_agent import compare_resume_to_job
import tempfile
import os

app = FastAPI(
    title="Resume Job Matcher API",
    description="API for parsing resumes, job postings, and comparing them",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/compare-resume-job/")
async def compare_resume_job(file: UploadFile = File(...), job_url: str = Form(...)):
    try:
        # Check if file is PDF
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Save and parse resume
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        try:
            # Parse resume
            parsed_resume = parse_resume(temp_path)

            # Parse job posting
            parsed_job = parse_job_link(job_url)

            # Compare resume and job
            comparison_result = compare_resume_to_job(parsed_resume, parsed_job)

            return {
                "parsed_resume": parsed_resume,
                "parsed_job": parsed_job,
                "comparison_result": comparison_result,
            }

        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except:
                pass

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
