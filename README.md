# 📚 AI-Powered Student Workspace

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://promtwarsproject.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gemini API](https://img.shields.io/badge/Google%20Gemini-Multimodal-orange.svg)](https://ai.google.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

> An intelligent, multimodal academic companion that transforms raw lecture slides, scanned documents, and study notes into structured, high-yield revision summaries and interactive practice quizzes.

🔗 **Live Deployment:** [https://promtwarsproject.streamlit.app](https://promtwarsproject.streamlit.app)  
📂 **GitHub Repository:** [https://github.com/YashRaoPatankar/PromtWarsProject](https://github.com/YashRaoPatankar/PromtWarsProject)

---

## 🌟 Key Features

- **📄 Multimodal Document Understanding:** Ingests native text and scanned/image-based PDFs directly via Gemini vision capabilities, completely eliminating OCR extraction failures on complex slide decks.
- **🎯 Contextual Role Prompting:** Dynamically adapts tutor personas and explanation depth based on chosen academic fields (e.g., *Computational & Data Science*, *Calculus*, *Physics*, *Python Programming*).
- **📝 High-Yield Revision Notes:** Distills dense academic materials into concise core formulas, critical definitions, theorems, and bulleted takeaways.
- **❓ Targeted Practice Quizzes:** Generates balanced 5-question multiple-choice quizzes with complete answer keys and conceptual explanations at the end.
- **💾 One-Click Export:** Instantly download generated revision notes and quizzes as clean Markdown (`.md`) files for offline revision or Notion/Obsidian integration.

---

## 🧠 Prompt Engineering Strategy

This workspace leverages tailored prompt engineering architectures:

1. **Domain-Specific Persona Conditioning:** System instructions frame the LLM as an expert academic tutor tailored to the specific course context selected by the student.
2. **Constrained Dual-Output Structuring:** Enforces a rigid two-tier response contract:
   - **Tier 1:** Condensed, formula-dense bullet points for rapid pre-exam review.
   - **Tier 2:** Formatted multiple-choice assessment items with hidden or appended answer logic to foster active recall.
3. **Multimodal Grounding:** Attaches raw document byte streams directly to the generation payload, ensuring diagrams, mathematical notations, and lecture layouts are interpreted faithfully without lossy text-only pre-parsing.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **LLM & Vision Engine:** [Google Gemini API](https://ai.google.dev/) (`google-generativeai`)
- **Document Processing:** Multimodal Byte Payloads (PDF) & `python-docx` (DOCX)
- **Containerization & Deployment:** Docker & Streamlit Community Cloud

---

## 🚀 Getting Started (Local Development)

### 1. Clone the Repository
```bash
git clone https://github.com/YashRaoPatankar/PromtWarsProject.git
cd PromtWarsProject
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY="your_google_ai_studio_api_key_here"
```

### 4. Run the Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 🐳 Docker Deployment

To build and run the container locally:

```bash
docker build -t student-workspace .
docker run -p 8080:8080 -e GEMINI_API_KEY="" student-workspace
```

---

## 👥 Authors & Acknowledgments

Built for the **Prompt Wars Hackathon** using Google Gemini and Streamlit.
