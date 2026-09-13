import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import docx

# Load environment configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()

if not api_key:
    st.error("⚠️ Missing GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(page_title="AI Student Workspace", page_icon="📚", layout="centered")
st.title("📚 AI-Powered Student Workspace")
st.write("Upload your study materials (PDF or DOCX) to get personalized revision notes and practice quizzes!")

course_context = st.selectbox(
    "Select your course context:",
    ["General", "Computational and Data Science", "Calculus", "Physics", "Python Programming"],
    help="Choose the subject area to tailor technical rigor and vocabulary."
)

uploaded_file = st.file_uploader(
    "Upload Document",
    type=['pdf', 'docx'],
    help="Upload lecture slide decks or notes (max 25MB)."
)

if uploaded_file is not None:
    # Security validation
    MAX_FILE_SIZE_MB = 25
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"File size exceeds {MAX_FILE_SIZE_MB}MB limit.")
        st.stop()

    if st.button("Generate Notes & Quiz", help="Analyze document and generate revision materials."):
        try:
            with st.spinner("Analyzing document with Gemini..."):
                # Dynamically fetch models authorized for this API key
                valid_models = [
                    m.name for m in genai.list_models() 
                    if 'generateContent' in m.supported_generation_methods
                ]
                
                # Prioritize flash / multimodal models
                target_model = None
                for candidate in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-2.0-flash', 'gemini-1.5-pro']:
                    for m in valid_models:
                        if candidate in m:
                            target_model = m
                            break
                    if target_model:
                        break

                if not target_model and valid_models:
                    target_model = valid_models[0]

                if not target_model:
                    st.error("No generation models found for this API key. Verify your Google AI Studio key.")
                    st.stop()

                model = genai.GenerativeModel(target_model)

                prompt = f"""
                You are an expert academic tutor for a student studying {course_context}.
                Analyze the attached document and provide:
                1. CONDENSED REVISION NOTES: Core formulas, key concepts, and summaries in bullet points.
                2. PRACTICE QUIZ: 5 multiple-choice questions (A-D) with the answer key and short explanations at the very end.
                """
                
                if uploaded_file.name.endswith('.pdf'):
                    contents = [
                        {"mime_type": "application/pdf", "data": uploaded_file.getvalue()},
                        prompt
                    ]
                else:
                    doc = docx.Document(uploaded_file)
                    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                    contents = [f"{prompt}\n\nDocument Text:\n{text}"]

                response = model.generate_content(contents)
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
                st.download_button(
                    label="Download Notes & Quiz (.md)",
                    data=response.text,
                    file_name=f"{uploaded_file.name}_revision.md",
                    mime="text/markdown",
                    help="Save the generated notes and quiz as a Markdown file."
                )
        except Exception as e:
            st.error(f"API Error: {e}")
            try:
                available = [m.name for m in genai.list_models()]
                st.info(f"Available models for this key: {available}")
            except Exception as inner_err:
                st.warning(f"Could not list models: {inner_err}")
