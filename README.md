# Resume Analyzer

A Streamlit application that analyzes resumes against job descriptions using the Groq API.

## Features

- Upload your resume in PDF format
- Enter a job description
- Get an AI-powered analysis of how well your resume matches the job requirements
- Receive suggestions for improving your resume

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/ayush3245/resume-analyzer.git
   cd resume-analyzer
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Groq API key:
   ```
   # Copy the example file
   cp .env.example .env

   # Then edit the .env file and replace with your actual API key
   GROQ_API_KEY=your_groq_api_key_here
   ```

   You can get a Groq API key by signing up at [console.groq.com](https://console.groq.com/)

4. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

5. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Requirements

- Python 3.8+
- Streamlit
- PyPDF2
- python-dotenv
- requests

## How It Works

1. The app extracts text from your uploaded PDF resume
2. It sends both the resume text and job description to the Groq API (using Llama 3 70B model)
3. The AI analyzes the match and provides detailed feedback
4. Results are displayed in the Streamlit interface

## Security Notes

- The `.env` file containing your API key is excluded from git via `.gitignore`
- Never commit API keys or other sensitive credentials to your repository
- Use the provided `.env.example` as a template for required environment variables

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request