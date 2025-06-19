# cold_message_generator/app.py
import streamlit as st
from utils.extract_text import extract_text_and_links
from utils.summarize_resume import extract_resume_summary
from utils.config import set_groq_api_key
from chains.message_chain import generate_message_template
from utils.format_message import format_message_with_placeholders
from models.schema import UserInput
import time


# --- SEO Friendly Page Configuration ---
st.set_page_config(
    page_title="Cold Message Generator - AI-Powered Outreach",
    page_icon="✍️", 
    layout="centered", 
    initial_sidebar_state="expanded", 
)
# --- End SEO Friendly Page Configuration ---

def display_temporary_message(message, duration=3):
    """Displays a message that disappears after a given duration.

    Args:
        message (str): The message to display.
        duration (int, optional): The duration in seconds for which the message is displayed.
                                Defaults to 3.
    """
    container = st.empty()
    container.info(message)
    time.sleep(duration)
    container.empty()

# 🔐 Sidebar for API Key
st.sidebar.title("🔑 API Configuration")
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

if api_key:
    set_groq_api_key(api_key)
    st.sidebar.success("API Key set successfully!")
else:
    st.sidebar.warning("Please enter your Groq API Key")

# 🧊 App Title
st.title("🧊 Cold Message Generator")

# Initialize session state variables if they don't exist
# This ensures that these keys always have a value on first run
if "summary" not in st.session_state:
    st.session_state["summary"] = ""
if "links" not in st.session_state:
    st.session_state["links"] = {}
if "template" not in st.session_state:
    st.session_state["template"] = ""
if "last_uploaded_file_id" not in st.session_state:
    st.session_state["last_uploaded_file_id"] = None


# --- Resume Upload and Processing Logic ---
st.subheader("Upload Resume or Paste Text")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# This block should ONLY calculate new values and set them to st.session_state
# It should NOT re-declare a widget or set a widget's value explicitly.
if uploaded_file and not api_key:
    st.warning("Enter Valid key")
if uploaded_file and api_key:
    # Check if a new file was uploaded to avoid reprocessing on every rerun
    if st.session_state["last_uploaded_file_id"] != uploaded_file.file_id:
        st.session_state["last_uploaded_file_id"] = uploaded_file.file_id # Update tracker

        with st.spinner("Extracting text and links..."):
            resume_text, extracted_links = extract_text_and_links(uploaded_file)
        display_temporary_message("Resume text and links extracted successfully.",duration=3)

        with st.spinner("Summarizing resume..."):
            # This is the key: set the session state value here
            summary_result = extract_resume_summary(resume_text)
            # Ensure the result is always a string
            st.session_state["summary"] = str(summary_result) if summary_result is not None else ""
        st.success("Resume summary generated.")

        # Also update links and clear template
        st.session_state["links"] = extracted_links if extracted_links else {}
        st.session_state["template"] = "" # Clear template on new resume upload


# --- Widget Definition for Summary ---
# Ensure the summary value is always a string before passing to text_area
summary_value = st.session_state.get("summary", "")
if not isinstance(summary_value, str):
    summary_value = str(summary_value) if summary_value is not None else ""

st.text_area(
    "Summary here:",
    value=summary_value, # This populates the text area with the current summary
    key="summary", # This connects the widget to st.session_state["summary"]
    height=150
)
# Any manual edits by the user in this text_area will update st.session_state["summary"]
# on the *next* script rerun.


# Social links - Populate from session state and allow user override
st.subheader("Links (auto-filled from resume if possible)")

# Ensure links dictionary exists and has string values
links = st.session_state.get("links", {})
if not isinstance(links, dict):
    links = {}

st.session_state["resume"] = st.text_input("Resume Link", value=links.get("resume", ""), key="resume_input")
st.session_state["linkedin"] = st.text_input("LinkedIn Link", value=links.get("linkedin", ""), key="linkedin_input")
st.session_state["github"] = st.text_input("GitHub Link", value=links.get("github", ""), key="github_input")
st.session_state["portfolio"] = st.text_input("Portfolio Link", value=links.get("portfolio", ""), key="portfolio_input")
st.session_state["blog"] = st.text_input("blogSite Link", value=links.get("blog", ""), key="blog_input")
message_type = st.selectbox("Message Type", ["Cold Email for referral","Cold email to connect","Cold Email for Job inquiry", "LinkedIn Message for refferal", "LinkedIn Message for career Guidance","LinkedIn Message for Job inquiry"], key="message_type_select")
job_type = st.text_input("Job Type:")

# Generate template
if st.button("Generate Template", key="generate_template_button"):
    if not api_key:
       display_temporary_message("Please enter your Groq API Key to generate a template.",duration=3)
    elif not st.session_state["summary"]:
        st.error("Please upload a resume or provide a summary before generating a template.")
    else:
        user_input = UserInput(
            summary=st.session_state["summary"],
            resume =st.session_state["resume"],
            linkedin=st.session_state["linkedin"],
            github=st.session_state["github"],
            portfolio=st.session_state["portfolio"],
            blog=st.session_state["blog"],
            message_type=message_type,
            job_type=job_type
        )
        with st.spinner("Generating message template..."):
            template = generate_message_template(user_input)
        st.session_state["template"] = template
        st.success("Template generated successfully!")


# Show template if available
if st.session_state["template"]:
    st.subheader("Template Preview")
    st.text_area("Template (with placeholders)", st.session_state["template"], height=200, key="template_preview")

    st.subheader("Recipient Details")
    recipient = st.text_input("Recipient Name", key="recipient_name")
    company = st.text_input("Company Name", key="company_name")

    if st.button("Generate Message", key="generate_message_button"):
        if not recipient or not company:
            st.warning("Please enter both Recipient Name and Company Name.")
        else:
            with st.spinner("Formatting final message..."):
                final_message = format_message_with_placeholders(st.session_state["template"], recipient, company)
            st.subheader("Generated Message")
            st.text_area("Message", final_message, height=300, key="final_message_output")
else:
    st.warning("Please generate a template first.")