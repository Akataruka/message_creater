from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from models.schema import LinkMap
from utils.config import get_groq_api_key


# Create parser for Pydantic output
parser = PydanticOutputParser(pydantic_object=LinkMap)

# Prompt template with format instructions injected
link_prompt = PromptTemplate(
    template="""You are an assistant that classifies URLs by platform.
Given this list of URLs, return a JSON object mapping platforms like LinkedIn, GitHub, Portfolio, Twitter, or Website to their full URLs.

If a platform is missing, use null for that key.

Links:
{links}

{format_instructions}
""",
    input_variables=["links"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

def classify_links_with_llm(link_list: list[str]) -> dict:
    
    GROQ_API_KEY = get_groq_api_key()

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,   # Replace with your actual API key or use env var
        model_name="llama3-70b-8192",       # Groq's LLaMA3 model
        temperature=1
    )
    formatted_links = "\\n".join(link_list)
    prompt = link_prompt.format(links=formatted_links)
    response = llm.invoke(prompt)
    try:
        return parser.parse(response.content).model_dump()
    except Exception as e:
        print("Parsing error:", e)
        return {}
    