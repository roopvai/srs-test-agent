import streamlit as st
import pandas as pd
from src.ingestion import parse_docx
from src.chunking import split_requirements
from src.generators import generate_test_cases, generate_edge_cases, generate_risks

st.set_page_config(page_title="SRS Test Agent", layout="wide")
st.title("AI Test Case & Risk Generator")
st.write("Upload a requirements document to generate test cases, edge cases, and quality risks.")

uploaded = st.file_uploader("Upload SRS document (.docx)", type=["docx"])

if uploaded and st.button("Analyze"):
    with open("temp.docx", "wb") as f:
        f.write(uploaded.getbuffer())
    text = parse_docx("temp.docx")
    requirements = split_requirements(text)
    st.success(f"Found {len(requirements)} requirements")

    all_tests, all_edges, all_risks = [], [], []
    progress = st.progress(0)
    status = st.empty()

    for i, req in enumerate(requirements):
        status.text(f"Processing {req['id']}...")
        tests = generate_test_cases(req)
        edges = generate_edge_cases(req, tests)
        risks = generate_risks(req, text)
        all_tests += [t.model_dump() for t in tests]
        all_edges += [e.model_dump() for e in edges]
        all_risks += [r.model_dump() for r in risks]
        progress.progress((i + 1) / len(requirements))

    status.text("Done.")
    tab1, tab2, tab3 = st.tabs(["Test Cases", "Edge Cases", "Quality Risks"])

    with tab1:
        df = pd.DataFrame(all_tests)
        st.dataframe(df)
        if not df.empty:
            st.download_button("Download CSV", df.to_csv(index=False), "test_cases.csv")

    with tab2:
        df = pd.DataFrame(all_edges)
        st.dataframe(df)
        if not df.empty:
            st.download_button("Download CSV", df.to_csv(index=False), "edge_cases.csv")

    with tab3:
        df = pd.DataFrame(all_risks)
        st.dataframe(df)
        if not df.empty:
            st.download_button("Download CSV", df.to_csv(index=False), "risks.csv")