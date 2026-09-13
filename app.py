import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import docx

# Load environment configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)

st.set_page_config(page_title="AI Student Workspace", page_icon="📚", layout="centered")
st.title("📚 AI-Powered Student Workspace")
st.write("Upload your study materials (PDF or DOCX) to get personalized revision notes and practice quizzes!")

course_context = st.selectbox(
    "Select your course context:",
    ["General", "Computational and Data Science", "Calculus", "Physics", "Python Programming"]
)

uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'docx'])

if uploaded_file is not None:
    if st.button("Generate Notes & Quiz"):
        try:
            with st.spinner("Analyzing document with Gemini..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
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
                    text = "\n".join([p.text for p in doc.paragraphs])
                    contents = [f"{prompt}\n\nDocument Text:\n{text}"]

                response = model.generate_content(contents)
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
                st.download_button(
                    label="Download Notes & Quiz (.md)",
                    data=response.text,
                    file_name=f"{uploaded_file.name}_revision.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"API Error: {e}")
