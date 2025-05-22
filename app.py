import streamlit as st
import pdfplumber
from docx import Document
import os
from io import StringIO
import requests  # <-- added

st.set_page_config(
    page_title="Advanced Text Extractor",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        h1 {
            color: #2c3e50;
            font-size: 2.5em;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            border-radius: 10px;
        }
        .stDownloadButton>button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 10px;
        }
        .stTextArea textarea {
            background-color: #ffffff;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

def extract_pdf_text(file):
    """Extracts text from PDF (all pages)."""
    full_text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n\n"
        return full_text.strip()
    except Exception as e:
        st.error(f"Failed to read PDF: {str(e)}")
        return None

def extract_docx_text(file):
    """Extracts text from DOCX files."""
    try:
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"Failed to read DOCX: {str(e)}")
        return None

def extract_txt_text(file):
    """Extracts text from TXT files."""
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Failed to read TXT: {str(e)}")
        return None

def save_text_to_file(text, filename):
    """Saves extracted text to a downloadable file."""
    output = StringIO()
    output.write(text)
    return output.getvalue().encode("utf-8")


def main():
    st.title("📄 Advanced Text Extractor")
    st.markdown("Upload a **PDF, DOCX, or TXT** file to extract its text.")

    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False
    )

    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        file_details = {
            "Name": uploaded_file.name,
            "Type": uploaded_file.type,
            "Size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.write(file_details)

        text = None
        if uploaded_file.type == "application/pdf":
            text = extract_pdf_text(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_docx_text(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text = extract_txt_text(uploaded_file)

        if text:
            st.subheader("Extracted Text")
            st.text_area("Content", text, height=300)

            st.download_button(
                label="📥 Download Text",
                data=save_text_to_file(text, uploaded_file.name),
                file_name=f"extracted_{os.path.splitext(uploaded_file.name)[0]}.txt",
                mime="text/plain"
            )

        # --- Upload to API ---
        try:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post("YOUR_API_ENDPOINT", files=files)

            if response.status_code == 200:
                st.success("File uploaded to API successfully!")
                # Optionally show response content here:
                # st.write(response.json())
            else:
                st.error(f"Upload failed: {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"Failed to upload file to API: {e}")

if __name__ == "__main__":
    main()
