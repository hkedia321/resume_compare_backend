from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.config import get_openai_api_key
import json

def compare_resume_to_job(resume_info, job_info):
    try:
        # Convert input data to string if it's a dict
        if isinstance(resume_info, dict):
            resume_info = json.dumps(resume_info, indent=2)
        if isinstance(job_info, dict):
            job_info = json.dumps(job_info, indent=2)
            
        # If inputs are JSON strings, try to parse and re-stringify them with proper formatting
        try:
            if isinstance(resume_info, str):
                resume_data = json.loads(resume_info)
                resume_info = json.dumps(resume_data, indent=2)
        except json.JSONDecodeError:
            pass  # Not valid JSON, use as is
            
        try:
            if isinstance(job_info, str):
                job_data = json.loads(job_info)
                job_info = json.dumps(job_data, indent=2)
        except json.JSONDecodeError:
            pass  # Not valid JSON, use as is
             
        prompt = PromptTemplate(
            input_variables=["resume", "job"],
            template="""You are an expert resume consultant and job matcher.

Compare the following resume and job posting. Dont give much weight to the preferred skills mentioned in the job posting. Provide a detailed analysis in JSON format with the following structure:
{{
    "match_score": number (0-100),
    "key_strengths": ["strength1", "strength2", ...],
    "areas_for_improvement": ["area1", "area2", ...],
    "resume_suggestions": ["suggestion1", "suggestion2", ...],
    "skills_to_develop": ["skill1", "skill2", ...]
}}
 
Resume Information:
{resume}

Job Information:
{job}

Provide a clear, actionable analysis in JSON format to help you improve your resume for this position."""
        )

        # Use the API key from config
        llm = ChatOpenAI(openai_api_key=get_openai_api_key(), temperature=0.2)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        result = chain.run(resume=resume_info, job=job_info)
        
        # Try to parse the result as JSON
        try:
            # Clean the response string to ensure it's valid JSON
            cleaned_result = result.strip()
            if cleaned_result.startswith('```json'):
                cleaned_result = cleaned_result[7:]
            if cleaned_result.endswith('```'):
                cleaned_result = cleaned_result[:-3]
            cleaned_result = cleaned_result.strip()
            
            parsed_result = json.loads(cleaned_result)
            return parsed_result
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse LLM response as JSON",
                "raw_response": result,
                "parse_error": str(e)
            }
        
    except Exception as e:
        return {
            "error": "Error comparing resume to job",
            "details": str(e)
        }
