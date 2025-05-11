import streamlit as st
from streamlit_tags import st_tags
import torch
import io

torch.classes.__path__ = []

if 'parser' not in st.session_state:
    from resume_analyzer import ResumeParser
    st.session_state.parser = ResumeParser()

if 'data' not in st.session_state:
    st.session_state.data = None

parser = st.session_state.parser
resume = st.file_uploader("Upload your resume", type=["pdf", "docx"], accept_multiple_files= False)
if not resume:
    st.stop()

parse_button = st.button("Parse Resume")
if parse_button:
    st.session_state.data = None
    resume_content = resume.read()
    resume_io = io.BytesIO(resume_content)
    resume_io.name = resume.name
    details = parser.parse(resume_io)
    st.session_state.data = details

if st.session_state.data:
    for key, value in st.session_state.data.items():
        if isinstance(value, list):
            keywords = st_tags(label=key, value= value)
            continue
        if isinstance(value, float) or isinstance(value, int):
            st.number_input(key, value= value)
            continue
        else:
            st.text_input(key, value)


