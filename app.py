import streamlit as st
from utils import extract_metadata

st.set_page_config(page_title="DocuTag - Metadata Generator", layout="wide")
st.title("DocuTag: Automated Metadata Extractor")

st.write("Upload a `.pdf`, `.docx`, or `.txt` file to extract structured metadata.")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()

    with st.spinner("Reading and processing the document..."):
        metadata = extract_metadata(uploaded_file, ext)

    st.success("Metadata extracted successfully!")

    st.subheader("Extracted Metadata")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Title:** {metadata['title']}")
        st.markdown(f"**Author:** {metadata['author']}")
        st.markdown(f"**Date:** {metadata['date']}")
    with col2:
        st.markdown(f"**Keywords:** {', '.join(metadata['keywords'])}")
        st.markdown(f"**Topics:** {', '.join(metadata['topics'])}")

    st.markdown("**Summary:**")
    st.info(metadata["summary"])

    st.subheader("Document Preview")
    st.text_area("Full Text", metadata["preview"], height=250)

    st.markdown("---")
