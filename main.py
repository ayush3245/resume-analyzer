import streamlit as st
import PyPDF2
import io
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Debug: Print masked API key to verify it's loaded
if GROQ_API_KEY:
    masked_key = GROQ_API_KEY[:4] + "*" * (len(GROQ_API_KEY) - 8) + GROQ_API_KEY[-4:] if len(GROQ_API_KEY) > 8 else "***"
    print(f"API Key loaded: {masked_key}")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def analyze_resume(resume_text, job_description):
    """Analyze resume against job description using Groq API"""

    # Check if API key is available
    if not GROQ_API_KEY:
        return "Error: Groq API key not found. Please set the GROQ_API_KEY environment variable."

    # Prepare the prompt for the LLM
    prompt = f"""
    You are an expert resume reviewer and career coach. Analyze the following resume against the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Provide a detailed analysis with the following sections:
    1. Match Score (0-100%)
    2. Key Strengths (skills and experiences that align well with the job)
    3. Gaps (important requirements from the job description that are missing or weak in the resume)
    4. Improvement Suggestions (specific recommendations to improve the resume for this job)
    5. Overall Assessment (brief summary of fit for the role)

    Format your response in markdown.
    """

    # Call Groq API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",  # Using Llama 3 70B model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 4000
    }

    try:
        print(f"Sending request to Groq API...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        # Print response status for debugging
        print(f"Response status code: {response.status_code}")

        # Handle specific error codes
        if response.status_code == 401:
            return "Error: Authentication failed. Please check your Groq API key."
        elif response.status_code == 400:
            error_detail = response.json().get("error", {}).get("message", "Bad request")
            return f"Error: Bad request - {error_detail}"

        response.raise_for_status()  # Raise exception for other HTTP errors

        result = response.json()
        analysis = result["choices"][0]["message"]["content"]
        return analysis

    except requests.exceptions.RequestException as e:
        return f"Network error calling Groq API: {str(e)}"
    except ValueError as e:
        return f"Error parsing JSON response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Resume Analyzer")
st.subheader("Compare your resume against a job description")

# Instructions
with st.expander("ℹ️ Instructions", expanded=False):
    st.markdown("""
    1. Upload your resume in PDF format
    2. Paste the job description in the text area
    3. Click 'Analyze Resume' to get feedback
    4. Make sure you have set your GROQ_API_KEY in the .env file
    """)

# File uploader for resume
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Text area for job description
job_description = st.text_area("Paste the job description here", height=300)

# API Key status indicator
if not GROQ_API_KEY:
    st.error("⚠️ Groq API key not found. Please add your API key to the .env file.")
else:
    st.success("✅ Groq API key loaded")

# Submit button
if st.button("Analyze Resume"):
    if not GROQ_API_KEY:
        st.error("Please set your Groq API key in the .env file before analyzing.")
    elif uploaded_file is not None and job_description:
        with st.spinner("Analyzing your resume..."):
            # Extract text from PDF
            resume_text = extract_text_from_pdf(uploaded_file)

            # Get analysis from Groq API
            analysis = analyze_resume(resume_text, job_description)

            # Display analysis
            st.markdown("## Analysis Results")
            st.markdown(analysis)
    else:
        st.error("Please upload a resume and provide a job description.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Groq API")