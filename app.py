import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def generate_study_material(text, course):
    prompt = f"""
You are an expert tutor for the course/subject: {course}.
Based on the provided document text, please generate the following two sections:

1. Condensed Revision Notes
   - Format with structured Markdown bullet points.
   - Summarize the key concepts clearly and concisely.

2. 5-Question Practice Quiz
   - Create 5 multiple-choice questions based on the text.
   - Place all the correct answers at the very bottom of the quiz.

Document Text:
{text}
"""
    # Determine the best available model
    available_models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if "gemini-3.6-flash" in available_models:
        model_name = "gemini-3.6-flash"
    elif "gemini-2.0-flash" in available_models:
        model_name = "gemini-2.0-flash"
    elif available_models:
        model_name = available_models[0]
    else:
        model_name = "gemini-3.6-flash"
        
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

st.set_page_config(page_title="AI-Powered Student Workspace", page_icon="📚")
st.title("📚 AI-Powered Student Workspace")

st.markdown("Upload your study materials (PDF or DOCX) to get personalized revision notes and practice quizzes!")

course_options = [
    'General',
    'Computational & Data Science',
    'Calculus',
    'Physics',
    'Python Programming'
]
selected_course = st.selectbox("Select your course context:", course_options)

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx"])

if "generated_content" not in st.session_state:
    st.session_state.generated_content = None

if uploaded_file is not None:
    if st.button("Generate Notes & Quiz"):
        st.info("Extracting text from the uploaded document...")
        text_content = ""
        
        try:
            if uploaded_file.name.endswith('.pdf'):
                text_content = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.name.endswith('.docx'):
                text_content = extract_text_from_docx(uploaded_file)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            
        if len(text_content.strip()) < 20:
            st.error("Could not extract readable text from this file. If it's a scanned document, please try a standard text PDF.")
        else:
            st.success("Document text extracted successfully!")
            
            if not API_KEY:
                st.error("GEMINI_API_KEY is not set. Please add it to your .env file.")
            else:
                with st.spinner("Generating your personalized study materials using Gemini 1.5 Flash..."):
                    try:
                        st.session_state.generated_content = generate_study_material(text_content, selected_course)
                    except Exception as e:
                        st.error(f"API Error: {e}")
                        
    if st.session_state.generated_content:
        st.markdown("---")
        st.markdown(st.session_state.generated_content)
        st.markdown("---")
        
        st.download_button(
            label="📥 Download Notes & Quiz (.md)",
            data=st.session_state.generated_content,
            file_name=f"study_material_{uploaded_file.name}.md",
            mime="text/markdown"
        )
else:
    # Clear session state if file is removed
    st.session_state.generated_content = None
