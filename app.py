import streamlit as st
import google.generativeai as genai
import pdfplumber

# Configure the Gemini API key
genai.configure(api_key="AIzaSyDU6r_QdEfmKCgN7DNS_NPJsSy1smMR2v8")
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the prompts for different sections
overview_prompt = """
You are an expert resume summarizer. Analyze the following resume text and create an 'Overview' section. 
This section should provide a brief professional summary of the candidate, including their key strengths, core competencies, and professional objectives.
"""

skills_prompt = """
You are an expert in extracting key skills from resumes. Read the following resume text and list the candidate's 'Key Skills' in bullet points. 
Focus on technical skills, soft skills, and relevant industry-specific abilities.
"""

experience_prompt = """
You are an expert in identifying professional experiences from resumes. Summarize the 'Professional Experience' section of the following resume text.
Highlight each job role with key responsibilities, achievements, and the impact the candidate made. Use bullet points under each job role for clarity.
"""

projects_prompt = """
You are an expert resume summarizer with a focus on project management and development. 
Analyze the following resume text and extract a 'Projects' section. For each project, mention the project name, a brief description, technologies used, the role of the candidate, and key achievements.
"""

education_prompt = """
You are an expert in extracting educational qualifications from resumes. Summarize the 'Education' section of the following resume text.
Include the degree obtained, the institution name, years attended, and any notable achievements or honors.
"""

certifications_prompt = """
You are an expert in identifying certifications and training in resumes. Extract the 'Certifications and Training' section from the following resume text.
For each certification or training, mention the name, the issuing organization, and the date it was obtained.
"""

strengths_prompt = """
You are an expert in analyzing resumes to identify key strengths. Analyze the following resume text and extract a 'Strengths' section.
Highlight the candidate's strongest skills, experiences, and qualities that make them a good fit for potential employers.
"""

improvement_prompt = """
You are an expert career advisor. Analyze the following resume text and provide a 'Scope of Improvement' section.
Suggest what could be improved in the candidate's profile or what's lacking. Focus on areas such as missing skills, experience gaps, or weak points that need enhancement.
"""

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

# Function to get the Gemini response
def get_gemini_response(prompt, extracted_text):
    try:
        response = model.generate_content([prompt + "\n\n" + extracted_text])
        return response.text
    except Exception as e:
        st.error(f"Error in Gemini API response: {e}")
        return "No summary available."

# Streamlit UI setup
st.set_page_config(page_title="Resume Summarizer")
st.header("Resume Summarizer with Gemini")
uploaded_file = st.file_uploader("Upload your resume (PDF format)...", type=['pdf'])

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    extracted_text = extract_text_from_pdf(uploaded_file)

    # Create buttons to generate different sections
    if st.button("Generate Overview"):
        overview = get_gemini_response(overview_prompt, extracted_text)
        st.subheader("Overview")
        st.write(overview)
    
    if st.button("Generate Key Skills"):
        skills = get_gemini_response(skills_prompt, extracted_text)
        st.subheader("Key Skills")
        st.write(skills)
    
    if st.button("Generate Professional Experience"):
        experience = get_gemini_response(experience_prompt, extracted_text)
        st.subheader("Professional Experience")
        st.write(experience)
    
    if st.button("Generate Projects"):
        projects = get_gemini_response(projects_prompt, extracted_text)
        st.subheader("Projects")
        st.write(projects)
    
    if st.button("Generate Education"):
        education = get_gemini_response(education_prompt, extracted_text)
        st.subheader("Education")
        st.write(education)
    
    if st.button("Generate Certifications and Training"):
        certifications = get_gemini_response(certifications_prompt, extracted_text)
        st.subheader("Certifications and Training")
        st.write(certifications)

    if st.button("Highlight Strengths"):
        strengths = get_gemini_response(strengths_prompt, extracted_text)
        st.subheader("Strengths")
        st.write(strengths)

    if st.button("Suggest Scope of Improvement"):
        improvement = get_gemini_response(improvement_prompt, extracted_text)
        st.subheader("Scope of Improvement")
        st.write(improvement)

else:
    st.info("Please upload a PDF resume file to summarize.")
