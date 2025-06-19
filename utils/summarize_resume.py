from typing import Optional
from langchain_groq import ChatGroq
from langchain.output_parsers import PydanticOutputParser
from pydantic import ValidationError
from models.summary import Summary 
from langchain.prompts import PromptTemplate
from utils.config import get_groq_api_key




parser = PydanticOutputParser(pydantic_object=Summary)

def extract_resume_summary(resume_text: str) -> str: # <--- Returns Summary object
    """
    Extract structured resume information using LLM with forced JSON output.

    Args:
        resume_text (str): The raw text content of the resume

    Returns:
        Summary: Structured resume data as a Pydantic model

    Raises:
        ValueError: If API key is not provided or found
        Exception: For API or parsing errors
    """
    GROQ_API_KEY = get_groq_api_key()
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set.")

    # Create system prompt with schema enforcement
    system_prompt_template = PromptTemplate(
        template="""You are an expert resume parser. Extract information from the resume text and return ONLY a valid JSON object matching this schema:

    {format_instructions}

    CRITICAL RULES:
    1. Return ONLY valid JSON - no markdown, explanations, or extra text, NO COMMENTS.
    2. All field names must match the schema exactly.
    3. Use null for missing optional fields, empty arrays [] for missing lists.
    4. Create a compelling 2-3 sentence professional_summary highlighting key strengths.
    5. Extract ALL technical skills (languages, frameworks, tools, technologies).
    6. For total_experience, use format like "2 years", "5+ years", "6 months".
    7. For career_level, choose: "Entry Level", "Mid Level", "Senior Level", or "Executive".
    8. Include full URLs with http:// or https:// prefix.
    9. For work_experience, *ensure all descriptions are within the 'key_responsibilities' array*. Do NOT include free-form strings outside of keys. Focus on quantifiable achievements when possible.
    10. Be thorough but only include information clearly stated or reasonably inferred.

    Resume Text:
    {resume_text}

    Respond with the JSON immediately.
    """, # <--- Added emphasis on work_experience rules
        input_variables=["resume_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0.1,
    )

    try:
        # Format the full prompt with resume text
        formatted_prompt = system_prompt_template.format(resume_text=resume_text)

        response_message = llm.invoke(formatted_prompt)

        # Parse the content of the AIMessage into the Pydantic object
        # This will return a Summary object
        parsed_summary = parser.parse(response_message.content)
        return parsed_summary.model_dump() # <--- Return the Pydantic object directly

    except ValidationError as ve:
        print(f"Pydantic Validation Error: {ve}")
        # Optionally re-raise or return a default/empty Summary object
        raise # Re-raise if you want the error to propagate
    except Exception as e:
        print(f"API or general error during summary extraction: {e}")
        raise # Re-raise for clarity

if __name__ == "__main__":
    sample_resume = """
    John Doe
    Senior Software Engineer
    Email: john.doe@email.com | Phone: +1-555-0123
    LinkedIn: https://linkedin.com/in/johndoe | GitHub: https://github.com/johndoe
    San Francisco, CA

    PROFESSIONAL SUMMARY
    Experienced full-stack software engineer with 6+ years developing scalable web applications.
    Expert in Python, React, and cloud technologies with a proven track record of leading teams
    and delivering high-impact projects that improved system performance by 40%.

    TECHNICAL SKILLS
    • Languages: Python, JavaScript, TypeScript, Java, SQL
    • Frameworks: React, Node.js, Django, Flask, Express
    • Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
    • Databases: PostgreSQL, MongoDB, Redis
    • Tools: Git, Jenkins, Terraform, Elasticsearch

    PROFESSIONAL EXPERIENCE
    Senior Software Engineer | TechCorp Inc. | Jan 2021 - Present
    • Lead development of microservices architecture serving 1M+ users daily
    • Implemented CI/CD pipelines reducing deployment time by 60%
    • Mentored 3 junior developers and conducted code reviews
    • Technologies: Python, React, AWS, PostgreSQL

    Software Engineer | StartupXYZ | Jun 2019 - Dec 2020
    • Developed React-based dashboard increasing user engagement by 35%
    • Built RESTful APIs handling 10K+ requests per minute
    • Collaborated with product team to define technical requirements

    EDUCATION
    Bachelor of Science in Computer Science
    University of California, Berkeley | 2019
    GPA: 3.8/4.0

    PROJECTS
    E-commerce Platform | 2023
    Full-stack web application with payment integration and inventory management
    Technologies: React, Node.js, PostgreSQL, Stripe API

    CERTIFICATIONS
    • AWS Certified Solutions Architect (2022)
    • Google Cloud Professional Developer (2021)

    ACHIEVEMENTS
    • Hackathon Winner - Best Technical Innovation (2022)
    • Employee of the Quarter - Q3 2021
    """

    try:
        # Test the extraction
        # Now 'result' will correctly be a Summary object
        result = extract_resume_summary(sample_resume)
        print("✅ Extraction successful!")
        print(f"Name: {result.full_name}")
        print(f"Email: {result.contact_info.email}")
        print(f"Experience: {result.total_experience}")
        print(f"Skills: {result.technical_skills[:5]}...")  # First 5 skills
        print(f"Career Level: {result.career_level}")
        print(f"\nProfessional Summary:\n{result.professional_summary}")

        # Test JSON output
        print(f"\n📄 Full JSON Output:\n{result.model_dump_json(indent=2)}")

    except Exception as e:
        print(f"❌ Error during main execution: {e}")