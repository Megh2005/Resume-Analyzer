import streamlit as st
import google.generativeai as genai
import pdfplumber
import os

# Configure the Gemini API key using environment variable
api_key = "AIzaSyCpMOrythR3tdbgu5zBHdzQcOzxZNS5-hE"

# Set custom page configuration with a favicon and layout settings
st.set_page_config(
    page_title="Resume Summarizer",
    page_icon="favi.png",  # Replace with your favicon path
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom styles for background image, layout, and colors
st.markdown("""
    <style>
        .main {
            background-image: url('https://i.pinimg.com/564x/79/49/e4/7949e4a1679a715dde1150bf0c2f6987.jpg');  /* Replace with your light-colored background image URL */
            background-size: cover;
            color: #333;
            padding: 1.5rem;
        }
        .st-expander {
            background-color: rgba(255, 255, 255, 0.8);  /* Light, semi-transparent background */
            border-radius: 8px;
            margin-bottom: 1rem;
            padding: 1rem;
        }
        .st-expander-header {
            font-size: 1.2rem;
            color: #4a4a4a;
            font-weight: bold;
        }
        .css-18e3th9 {padding: 0 5rem;}  /* Adds padding around the main content */
        .stTextInput > div > div > input {
            border: 2px solid #4a90e2;  /* Input border color */
        }
        .stButton > button {
            background-color: #4a90e2;  /* Button background color */
            color: white;
            border: none;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #357ABD;  /* Button hover effect */
            transition: 0.3s;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #4a90e2;
            color: white;
            text-align: center;
            padding: 1rem 0;
        }
        .footer a {
            color: white;
            text-decoration: none;
        }
        /* Change header text color to black */
        .css-1ujw7ow {
            color: #0f0f0f;  /* Black text color */
        }
        /* Change text color in st.info */
        .stAlert p {
            color: #333;  /* Darker text color */
            font-weight: bold;  /* Make the text bold for better visibility */
        }
    </style>
    """, unsafe_allow_html=True)

# Check if the API key is set
if not api_key:
    st.error("API key is not set. Please set the GEMINI_API_KEY environment variable.")
else:
    # Configure the Gemini API with the environment variable
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prompts for different sections
    overview_prompt = """
    You are an expert resume summarizer. Analyze the following resume text and create an 'Overview' section. 
    This section should provide a brief professional summary of the candidate, including their key strengths, core competencies, and professional objectives.
    """

    skills_prompt = """
    You are an expert in extracting key skills from resumes. Read the following resume text and list the candidate's 'Key Skills' in bullet points. 
    Focus on technical skills, soft skills, and relevant industry-specific abilities.
    """

    experience_prompt = """
    You are an expert in summarizing professional experience. Analyze the resume text and create a 'Professional Experience' section. 
    Highlight the most relevant job roles, responsibilities, and achievements, focusing on impact and results.
    """

    education_prompt = """
    You are an expert in summarizing educational background from resumes. Extract and summarize the 'Education' section, including degrees, 
    institutions, and key achievements or honors.
    """

    certifications_prompt = """
    You are an expert in identifying certifications and courses from resumes. List the 'Certifications and Courses' the candidate has completed. 
    Include the certification name, issuing organization, and date of completion if available.
    """

    strengths_weaknesses_prompt = """
    Provide a detailed analysis of the candidate's strengths and weaknesses based on their resume.
    Highlight areas where the candidate excels and where they could improve.
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
    st.markdown("<h1 style='color: black;'>📄 Resume Analyzer</h1>", unsafe_allow_html=True)
    st.write("""
    <p style="color:#000;">Enhance your professional profile by extracting key insights from your resume. Upload your resume in PDF format and let our AI model summarize it into 
    easy-to-read sections. From key skills to professional experience, get everything at a glance!</p>
    """, unsafe_allow_html=True)

    # Sidebar setup
    st.sidebar.image("logo.jpeg", use_column_width=True)  # Replace with your logo path
    st.sidebar.title("Guide")
    st.sidebar.write("""
    **Welcome to the Resume Analyzer!** Here's how to use the application:

    1. **Upload Your Resume:** Click on the "Upload your resume (PDF format)..." button to upload your resume. Ensure your resume is in PDF format.

    2. **Generate Sections:** Once the resume is uploaded, you can generate various sections of the resume:
        - **Overview:** Get a brief professional summary of the candidate.
        - **Key Skills:** Extract and list key skills mentioned in the resume.
        - **Professional Experience:** Summarize the candidate's professional experience, focusing on roles, responsibilities, and achievements.
        - **Education Summary:** Extract and summarize the educational background, including degrees and key achievements.
        - **Certifications and Courses:** List any certifications or courses the candidate has completed.
        - **Strengths and Weaknesses:** Get an analysis of the candidate's strengths and weaknesses.

    3. **Explore Additional Sections:** You can also view additional tips and resources related to resume writing and career development.

    **About the AI Model:**
    Our AI model leverages advanced generative capabilities to analyze your resume and provide detailed summaries for various sections. It uses natural language processing to understand and extract key information, helping you present a polished and professional profile.

    **Need Help?** If you encounter any issues or have questions, please contact us at [support@example.com](mailto:support@example.com).
    """)

    # File upload widget
    uploaded_file = st.file_uploader("Upload your resume (PDF format)...", type=['pdf'])

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        extracted_text = extract_text_from_pdf(uploaded_file)

        # Use expander widgets for better organization
        with st.expander("Generate Overview"):
            overview = get_gemini_response(overview_prompt, extracted_text)
            st.write(overview)
        
        with st.expander("Generate Key Skills"):
            skills = get_gemini_response(skills_prompt, extracted_text)
            st.write(skills)

        with st.expander("Generate Professional Experience"):
            experience = get_gemini_response(experience_prompt, extracted_text)
            st.write(experience)

        with st.expander("Generate Education Summary"):
            education = get_gemini_response(education_prompt, extracted_text)
            st.write(education)

        with st.expander("Generate Certifications and Courses"):
            certifications = get_gemini_response(certifications_prompt, extracted_text)
            st.write(certifications)
        
        with st.expander("Generate Strengths and Weaknesses Analysis"):
            strengths_weaknesses = get_gemini_response(strengths_weaknesses_prompt, extracted_text)
            st.write(strengths_weaknesses)

        # Additional expanders with newly styled sections
        with st.expander("Additional Tips and Career Advice"):
            st.write("""
            Here are some general tips to improve your resume:
            - Focus on quantifiable achievements.
            - Use action verbs and concise language.
            - Tailor your resume to the specific job you are applying for.
            """)

        # Additional Resources Section
        st.markdown("## 📘 Additional Resources")
        st.markdown("""
        - **Resume Writing Guide**: Learn the essentials of crafting a compelling resume.
        - **Career Development Tips**: Enhance your career with expert advice on growth and development.
        """)

        # Footer with links to the creator's profiles
        st.markdown("""
        <div class="footer">
            <p>Created by Sayambar Roy Chowdhury | <a href="https://www.linkedin.com/in/sayambar-roy-chowdhury-731b0a282/" target="_blank">LinkedIn</a> | <a href="https://github.com/Sayambar2004" target="_blank">GitHub</a></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Please upload a PDF resume file to summarize.")
