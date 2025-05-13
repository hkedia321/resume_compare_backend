from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.pdf_utils import extract_text_from_pdf
from utils.config import get_openai_api_key

def parse_resume(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)

    prompt = PromptTemplate(
        input_variables=["resume"],
        template="""
            You are an expert resume parser.

            Parse the following resume text and return a structured JSON with the following fields:

            - full_name
            - email
            - phone_number
            - linkedin
            - github
            - portfolio_website
            - education (list of degrees with university name and years)
            - skills (as a list)
            - work_experience (list of jobs, each with title, company, start_date, end_date, and responsibilities)
            - projects (if any, with title and description)
            - certifications (if any)
            - summary (a brief summary of the candidate)

            Resume Text:
            {resume}
            """
    )

    # Use the API key from config
    llm = ChatOpenAI(openai_api_key=get_openai_api_key())
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(resume=resume_text)
