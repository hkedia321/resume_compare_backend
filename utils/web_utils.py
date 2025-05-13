import requests
from bs4 import BeautifulSoup
import json
import re

def extract_text_from_url(url):
    try:
        # Special handling for LinkedIn job URLs
        if 'linkedin.com/jobs/view/' in url:
            # Extract job ID from the URL using regex
            job_id_match = re.search(r'linkedin\.com/jobs/view/(\d+)', url)
            if job_id_match:
                job_id = job_id_match.group(1)
                return extract_linkedin_job_by_id(job_id, url)
        
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Default parsing for other websites
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        return soup.get_text(separator="\n").strip()
    
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error processing URL: {str(e)}"

def extract_linkedin_job_by_id(job_id, original_url):
    """
    Alternative approach for LinkedIn jobs - create a static job description since
    we cannot reliably scrape LinkedIn job details
    """
    # First try with the normal scraping approach one more time
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
        }
        
        # Try using a different URL format
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        response = requests.get(job_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_element = soup.find('h1', class_='top-card-layout__title')
            title = title_element.text.strip() if title_element else "Unknown Position"
            
            # Extract company
            company_element = soup.find('a', class_='topcard__org-name-link')
            company = company_element.text.strip() if company_element else "Unknown Company"
            
            # Extract location
            location_element = soup.find('span', class_='topcard__flavor--bullet')
            location = location_element.text.strip() if location_element else "Unknown Location"
            
            # Extract description
            description_element = soup.find('div', class_='show-more-less-html__markup')
            description = description_element.get_text(separator="\n").strip() if description_element else ""
            
            # Compile all information
            job_info = f"""
            Job Title: {title}
            Company: {company}
            Location: {location}
            
            Job Description:
            {description}
            
            Original URL: {original_url}
            """
            
            return job_info
    except Exception as e:
        pass  # Silently fail and continue to fallback
    
    # If scraping failed, provide a job description template and instructions
    return f"""
    Unable to automatically extract the job details from LinkedIn for job ID: {job_id}.
    
    LinkedIn restricts access to their job listings through web scraping.
    
    To proceed, please:
    1. Open the job listing URL: {original_url}
    2. Copy the job details manually
    3. Paste them into the system, or
    4. Use a different job source that doesn't have these restrictions
    
    If you'd like to continue with this job, please provide the job details manually.
    """

def extract_linkedin_job(html_content):
    """
    Try various methods to extract LinkedIn job details from HTML content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Method 1: Try to extract the job description from standard class
    job_description = soup.find('div', class_='description__text')
    if job_description:
        return job_description.get_text(separator="\n").strip()
    
    # Method 2: Look for the show-more-less-html div
    description_div = soup.find('div', class_='show-more-less-html__markup')
    if description_div:
        return description_div.get_text(separator="\n").strip()
    
    # Method 3: Look for any divs that might contain job descriptions
    job_details = soup.find('div', {'id': 'job-details'})
    if job_details:
        return job_details.get_text(separator="\n").strip()
    
    # Method 4: If we couldn't find specific job elements, try to get main content
    main_content = soup.find('main')
    if main_content:
        return main_content.get_text(separator="\n").strip()
    
    # Method 5: Last resort, check for any large text blocks
    paragraphs = soup.find_all('p')
    if paragraphs and len(paragraphs) > 3:
        return "\n\n".join([p.get_text() for p in paragraphs])
    
    # Method 6: Remove scripts and styles and get all text
    for script in soup(["script", "style"]):
        script.extract()
    
    text = soup.get_text(separator="\n").strip()
    if len(text) > 200:  # Only return if we have substantial content
        return text
    
    # If all else fails, return a helpful message
    return "Could not extract job details from LinkedIn. Please provide the job description manually."
