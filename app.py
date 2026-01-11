from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------- CONFIG ----------
st.set_page_config(
    page_title="ATS Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.main {
    background-color: #0f172a;
}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #1f2937;
}
.title {
    font-size: 42px;
    font-weight: bold;
}
.subtitle {
    color: #9ca3af;
}
.highlight {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)


# ---------- FUNCTIONS ----------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_ai_analysis(resume_text, job_desc, mode):
    model = genai.GenerativeModel('gemini-pro')


    if mode == "Full Analysis":
        prompt = f"""
You are a professional ATS system and senior recruiter.

Analyze this resume vs job description and provide output in this structure:

1. ATS Match Score (0–100)
2. Strengths (bullet points)
3. Missing Keywords
4. Skills Gap
5. Resume Improvements
6. Final Verdict

Resume:
{resume_text}

Job Description:
{job_desc}
"""
    else:
        prompt = f"""
Only calculate ATS Match Score (0-100) and list missing keywords.

Resume:
{resume_text}

Job Description:
{job_desc}
"""

    response = model.generate_content(prompt)
    return response.text


# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("⚙ Settings")
    analysis_type = st.radio("Choose Mode", ["Full Analysis", "Quick ATS Scan"])
    st.markdown("---")
    st.markdown("Built with Gemini + Streamlit")
    st.markdown("👨‍💻 Portfolio-grade Project")


# ---------- MAIN UI ----------
st.markdown("<div class='title'>📄 ATS Resume Analyzer <span class='highlight'>Pro</span></div>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Smarter resume feedback powered by AI</p>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Job Description")
    job_description = st.text_area("Paste job description", height=250)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📎 Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("")

if st.button("🚀 Analyze Resume", use_container_width=True):
    if not uploaded_file or not job_description:
        st.error("Please upload resume and paste job description.")
    else:
        with st.spinner("AI is analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = get_ai_analysis(resume_text, job_description, analysis_type)

        st.markdown("---")
        st.subheader("📊 Analysis Report")
        st.markdown(result)

        st.download_button(
            "📥 Download Report",
            data=result,
            file_name="ATS_Report.txt"
        )


st.markdown("---")
st.caption("⚡ Built for serious job seekers | ATS-style evaluation using AI")
