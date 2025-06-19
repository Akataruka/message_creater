# 🧊 Cold Message Generator

## Project Overview

The **Cold Message Generator** is an AI-powered Streamlit application designed to help users quickly craft personalized cold outreach messages (like emails or LinkedIn messages). By leveraging large language models (LLMs) from Groq, it intelligently extracts key information from resumes (PDFs) and uses user-defined details to generate compelling, professional message templates. These templates can then be easily customized with recipient-specific information.

This tool aims to streamline the outreach process for job seekers, recruiters, or anyone needing to send personalized cold messages efficiently.

## ✨ Features

* **Resume Text and Link Extraction:** Upload PDF resumes, and the application will extract text content and identify relevant social links (LinkedIn, GitHub, Portfolio).
* **Intelligent Link Classification:** Utilizes a mechanism to classify hidden or ambiguous links found within the resume text.
* **AI-Powered Resume Summarization:** Uses an LLM to generate a concise, professional summary from the extracted resume text, adhering to a structured Pydantic schema for consistency.
* **Customizable Message Generation:** Generates tailored cold email or LinkedIn message templates based on the resume summary, extracted links, target job type, and desired message type.
* **Placeholder-Based Templating:** Outputs message templates with dynamic placeholders (e.g., `{{recipient_name}}`, `{{company_name}}`) that can be easily filled in.
* **User-Friendly Interface:** Built with Streamlit for an intuitive and interactive user experience.
* **Groq API Integration:** Leverages Groq's fast and powerful LLMs for efficient text processing and generation.

## 🚀 Technologies Used

* **Python 3.9+**
* **Streamlit:** For building the interactive web application.
* **LangChain:** For orchestrating LLM calls, managing prompts, and parsing outputs.
* **Groq API:** The underlying LLM provider (using models like `llama-3.1-70b-versatile` or `llama3-70b-8192`).
* **Pydantic:** For defining robust data schemas and parsing LLM outputs into structured objects.
* **`pypdf`:** (Assumed for PDF text extraction) For handling PDF files.
* **`re` (Python's regex module):** For text cleaning and link extraction.

## ⚙️ Setup and Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

* Python 3.9 or higher installed.
* A Groq API Key. You can obtain one from [Groq Console](https://console.groq.com/keys).

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/cold-message-generator.git](https://github.com/your-username/cold-message-generator.git)
    cd cold-message-generator
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (If `requirements.txt` doesn't exist, you'll need to create it by running `pip freeze > requirements.txt` after manually installing the core libraries: `streamlit`, `langchain`, `langchain-groq`, `pydantic`, `pypdf`.)

5.  **Configure your Groq API Key:**
    The application primarily takes the Groq API Key via a text input in the Streamlit sidebar. However, for programmatic access or if you prefer environment variables for deployment, ensure `GROQ_API_KEY` is set.
    *The `utils/config.py` file is intended to manage API keys; ensure it's set up to load the key either from an environment variable or a secure local configuration.*

6.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    This command will open the application in your default web browser.

## 🚀 Usage

1.  **Enter your Groq API Key:** Start by entering your Groq API Key in the sidebar on the left.
2.  **Upload Resume:** Use the "Upload your resume (PDF)" file uploader to provide your resume. The app will automatically extract text, identify and classify links, and generate a professional summary.
3.  **Review Summary and Links:** Check the extracted "Summary" and pre-filled "Links" sections. You can edit the summary or links if needed.
4.  **Select Message Type:** Choose whether you want a "Cold Email" or "LinkedIn Message" from the dropdown.
5.  **Enter Target Job Type:** Provide the specific job role you are targeting (e.g., "Software Engineer", "Data Scientist"). This helps the AI tailor the message.
6.  **Generate Template:** Click the "Generate Template" button. The AI will create a message template with `{{recipient_name}}` and `{{company_name}}` placeholders.
7.  **Fill Recipient Details:** Enter the actual "Recipient Name" and "Company Name".
8.  **Generate Final Message:** Click "Generate Message" to get the complete, personalized outreach message.
9.  **Copy and Send!** Copy the generated message and use it in your outreach.

## 📁 Project Structure

```
.
├── app.py                      # Main Streamlit application file
├── chains/                     # Contains LLM chain definitions and prompt logic
│   └── message_chain.py        # Logic for generating message templates
├── models/                     # Pydantic models for data schema
│   └── schema.py               # Defines UserInput schema
│   └── summary.py              # Defines Summary schema for resume extraction
├── utils/                      # Helper functions
│   ├── classify_links.py       # Logic for identifying and classifying hidden links in text
│   ├── config.py               # Handles configuration, including API key loading
│   ├── extract_text.py         # Functions for extracting raw text and links from PDFs
│   ├── format_message.py       # Utility for formatting final messages with placeholders
│   └── summarize_resume.py     # Logic for summarizing resumes using LLM
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
