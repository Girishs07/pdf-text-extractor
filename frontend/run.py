import streamlit as st
from docx import Document
import os
import io 
from io import StringIO
import requests

# Configure Streamlit page
st.set_page_config(
    page_title="Advanced Text Extractor",
    page_icon="📄",
    layout="wide"
)

# Backend API URL - Update this with your deployed backend URL
BACKEND_URL = "https://your-backend-name.onrender.com"  # Replace with actual URL

# Custom CSS styling
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
        .success-box {
            padding: 10px;
            border-radius: 5px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            margin: 10px 0;
        }
        .error-box {
            padding: 10px;
            border-radius: 5px;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

def extract_pdf_via_api(uploaded_file):
    """Extract text from PDF using the backend API"""
    try:
        # Prepare file for API request
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        # Make API request
        with st.spinner("🔄 Processing PDF via API..."):
            response = requests.post(
                f"{BACKEND_URL}/extract-pdf", 
                files=files,
                timeout=300  # 5 minutes timeout
            )

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ PDF processed successfully! Extracted {result.get('characters_extracted', 0)} characters from {result.get('pages_processed', 0)} pages.")
            return result.get("extracted_text", "")
        else:
            error_msg = response.json().get("detail", "Unknown error") if response.headers.get('content-type') == 'application/json' else response.text
            st.error(f"❌ API Error ({response.status_code}): {error_msg}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("🚫 Request timed out. The PDF might be too large or complex.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🚫 Failed to connect to the API. Please check if the backend service is running.")
        return None
    except Exception as e:
        st.error(f"🚫 Unexpected error: {str(e)}")
        return None

def extract_docx_text(file):
    """Extract text from DOCX file"""
    try:
        with st.spinner("🔄 Processing DOCX file..."):
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            st.success("✅ DOCX file processed successfully!")
            return text
    except Exception as e:
        st.error(f"Failed to read DOCX: {str(e)}")
        return None

def extract_txt_text(file):
    """Extract text from TXT file"""
    try:
        with st.spinner("🔄 Processing TXT file..."):
            text = file.read().decode("utf-8")
            st.success("✅ TXT file processed successfully!")
            return text
    except Exception as e:
        st.error(f"Failed to read TXT: {str(e)}")
        return None

def save_text_to_file(text, filename):
    """Prepare text for download"""
    output = StringIO()
    output.write(text)
    return output.getvalue().encode("utf-8")

def main():
    st.title("📄 Advanced Text Extractor")
    st.markdown("Upload a **PDF, DOCX, or TXT** file to extract its text content.")
    
    # Add backend status check
    with st.sidebar:
        st.header("🔧 System Status")
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend API is online")
            else:
                st.error("❌ Backend API issues")
        except:
            st.error("❌ Backend API is offline")
        
        st.markdown("---")
        st.markdown("**Supported formats:**")
        st.markdown("- 📄 PDF files")
        st.markdown("- 📝 DOCX files") 
        st.markdown("- 📃 TXT files")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False,
        help="Select a PDF, DOCX, or TXT file to extract text from"
    )

    if uploaded_file:
        # Display file information
        st.markdown("### 📋 File Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            st.metric("File Size", f"{uploaded_file.size / 1024:.2f} KB")
        with col3:
            st.metric("File Type", uploaded_file.type)

        text = None

        # Process different file types
        if uploaded_file.type == "application/pdf":
            text = extract_pdf_via_api(uploaded_file)
            
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_docx_text(uploaded_file)
            
        elif uploaded_file.type == "text/plain":
            text = extract_txt_text(uploaded_file)
        else:
            st.error("❌ Unsupported file type!")

        # Display extracted text and download option
        if text and text.strip():
            st.markdown("### 📖 Extracted Text")
            
            # Show text statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Characters", len(text))
            with col2:
                st.metric("Words", len(text.split()))
            with col3:
                st.metric("Lines", len(text.split('\n')))
            
            # Text area with extracted content
            st.text_area(
                "Content Preview", 
                text, 
                height=400,
                help="Scroll to view all extracted text"
            )

            # Download button
            st.download_button(
                label="📥 Download Extracted Text",
                data=save_text_to_file(text, uploaded_file.name),
                file_name=f"extracted_{os.path.splitext(uploaded_file.name)[0]}.txt",
                mime="text/plain",
                help="Download the extracted text as a .txt file"
            )
        elif text is not None:
            st.warning("⚠️ No text content found in the uploaded file.")

if __name__ == "__main__":
    main()