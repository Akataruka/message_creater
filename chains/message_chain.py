from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from models.schema import UserInput
from utils.config import get_groq_api_key




# Revised Prompt Template
# The prompt now explicitly asks for a Python-formatted string
# It treats the UserInput as a JSON string to guide the LLM
message_prompt = PromptTemplate.from_template(
    """You are an expert at crafting professional outreach messages.
Given the following user details and requested message type, generate a concise and compelling {message_type}.

User Details (JSON format for clarity):
{user_input_json}

The message MUST use Python f-string style placeholders for the recipient's name `{{recipient_name}}` and the company name `{{company_name}}`.

Focus on:
- Always mention a short, crisp subject on top and be respectful.
- Highlighting relevant skills from the summary for the {job_type} role.
- Clearly stating the purpose of the message.
- Including relevant links (resume, LinkedIn, GitHub, Portfolio) on the bottom point wise.
- Maintaining a professional and engaging tone.
- Be to the point , No Bluffing

Return ONLY the complete message content. Do NOT include any other text, formatting (like markdown code blocks), or explanations.
"""
)

def generate_message_template(user_input: UserInput) -> str:
    # Convert the UserInput Pydantic model to a JSON string
    # This helps the LLM understand the structured input better
    user_input_json_str = user_input.model_dump_json(indent=2) # Use indent for readability if LLM sees it

    # Format the prompt with the stringified user input
    # Also pass job_type for more specific message generation
    prompt_formatted = message_prompt.format(
        user_input_json=user_input_json_str,
        message_type=user_input.message_type,
        job_type=user_input.job_type # Pass job_type from the UserInput object
    )
    GROQ_API_KEY = get_groq_api_key()

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0.8 # Increased temperature slightly for more creative message generation
    )

    # Invoke the LLM
    response_message = llm.invoke(prompt_formatted)

    # The LLM is instructed to return only the message content
    return response_message.content

# Example Usage (for testing)
if __name__ == "__main__":
    # Create a dummy UserInput object
    test_user_input = UserInput(
        summary="Highly motivated and detail-oriented computer science student with experience in web applications, medical imaging, and team leadership. Proficient in a range of programming languages and frameworks, with a strong passion for problem-solving and collaboration.",
        linkedin="https://linkedin.com/in/asutosh-kataruka",
        github="https://github.com/Akataruka",
        portfolio="https://asutosh-kataruka.vercel.app/",
        message_type="Cold Email",
        job_type="Software Engineer"
    )

    print("Generating message template...")
    template = generate_message_template(test_user_input)
    print("\n--- Generated Template ---")
    print(template)

    