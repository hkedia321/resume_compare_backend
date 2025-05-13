from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.web_utils import extract_text_from_url

def parse_job_link(url):
    job_text = extract_text_from_url(url)
    
    prompt = PromptTemplate(
        input_variables=["job"],
        template="""
        You are an expert job description analyzer.
        
        Extract the following information from this job posting:
        - job_title
        - company_name
        - location
        - required_skills (as a list)
        - preferred_skills (as a list, if mentioned)
        - experience_required
        - education_required
        - job_description_summary
        - responsibilities (as a list)
        - qualifications (as a list)
        
        Return the information in a clean JSON format.
        
        Job Posting:
        {job}
        """
    )

    chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)
    return chain.run(job=job_text)
