import streamlit as st
from docx import Document
import os
import io 
from io import StringIO
import requests

st.set_page_config(
    page_title="Advanced Text Extractor",
    page_icon="📄",
    layout="wide"
)

BACKEND_URL = "https://pdf-textextractor.onrender.com" 

st.markdown("""
    <style>
        /* Modern color palette */
        :root {
            --primary: #0f172a;
            --secondary: #1e293b;
            --accent: #3b82f6;
            --accent-light: #60a5fa;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }
        
        /* Main app styling - Modern dark/light background */
        .main {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 2.5rem 1.5rem;
        }
        
        /* Header styling - Modern minimalist */
        .main-header {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 3rem 2.5rem;
            border-radius: 20px;
            box-shadow: 0 2px 20px rgba(0, 15, 45, 0.08);
            margin-bottom: 3rem;
            text-align: center;
            border: 1px solid rgba(51, 65, 85, 0.05);
            backdrop-filter: blur(10px);
        }
        
        .main-header h1 {
            color: #0f172a;
            font-size: 3.5em;
            margin-bottom: 0.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-header p {
            color: #64748b;
            font-size: 1.25em;
            font-weight: 500;
            margin: 0.75rem 0 0 0;
        }
        
        /* File uploader styling - Modern card */
        .stFileUploader {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 2px 16px rgba(0, 15, 45, 0.08);
            margin: 1.5rem 0;
            border: 2px dashed rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 4px 24px rgba(59, 130, 246, 0.12);
        }
        
        /* Button styling - Modern primary buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 15px;
            font-weight: 600;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Download button - Modern secondary */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 15px;
            font-weight: 600;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
        }
        
        /* Text area styling - Modern code editor look */
        .stTextArea textarea {
            background: #f8fafc;
            border: 1.5px solid #e2e8f0;
            border-radius: 12px;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 13px;
            color: #0f172a;
            padding: 16px;
            transition: all 0.3s ease;
        }
        
        .stTextArea textarea:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Metric cards - Modern minimal */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 1.75rem;
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(0, 15, 45, 0.06);
            text-align: center;
            border: 1px solid rgba(51, 65, 85, 0.05);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 15, 45, 0.12);
        }
        
        /* Sidebar styling - Modern dark sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        [data-testid="stSidebar"] .css-1d391kg {
            background: transparent;
        }
        
        /* Success styling */
        .stSuccess {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border-left: 4px solid #10b981;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
        }
        
        /* Error styling */
        .stError {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 4px solid #ef4444;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.15);
        }
        
        /* Warning styling */
        .stWarning {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
        }
        
        /* Info styling */
        .stInfo {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
        }
        
        /* Loading animation - Smooth pulse */
        .loading-text {
            font-size: 1.1em;
            color: #3b82f6;
            font-weight: 500;
            animation: smoothPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes smoothPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        /* Headings - Modern typography */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.01em;
        }
        
        h2 {
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.75em;
        }
        
        h3 {
            font-size: 1.35em;
            color: #1e293b;
        }
        
        /* Divider - Subtle */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(51, 65, 85, 0.2), transparent);
            margin: 2rem 0;
        }
        
        /* Code blocks - Modern dark */
        .stCodeBlock {
            background: #1e293b !important;
            border-radius: 12px !important;
            border: 1px solid rgba(51, 65, 85, 0.3) !important;
        }
        
        /* Expander - Modern */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid rgba(51, 65, 85, 0.05);
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        /* Slider styling - Modern */
        .stSlider > div > div > div {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        }
        
        /* Tab styling - Modern */
        .stTabs [role="tablist"] {
            gap: 1rem;
            background: transparent;
        }
        
        .stTabs [role="tab"] {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid rgba(51, 65, 85, 0.1);
            border-radius: 10px 10px 0 0;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            color: #64748b;
            transition: all 0.3s ease;
        }
        
        .stTabs [role="tab"][aria-selected="true"] {
            background: white;
            color: #3b82f6;
            border-color: #3b82f6;
        }
    </style>
""", unsafe_allow_html=True)

def extract_pdf_via_api(uploaded_file):
    """Extract text from PDF using the backend API with robust error handling"""
    try:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > 100:
            st.error(f"❌ File too large: {file_size_mb:.1f}MB. Maximum allowed: 100MB")
            return None
        
        uploaded_file.seek(0)
        
        files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔄 Connecting to backend...")
            progress_bar.progress(25)
            response = requests.post(
                f"{BACKEND_URL}/extract-pdf", 
                files=files,
                timeout=300  
            )
            status_text.text("🔄 Processing PDF...")
            progress_bar.progress(75)
    
            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")
            
            import time
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
        except requests.exceptions.Timeout:
            progress_bar.empty()
            status_text.empty()
            st.error("🚫 **Request timed out** - The PDF might be too large or complex. Try a smaller file or try again later.")
            return None
        except requests.exceptions.ConnectionError:
            progress_bar.empty()
            status_text.empty()
            st.error("🚫 **Connection failed** - Backend service might be sleeping. Please wait 30 seconds and try again.")
            
            # Add retry button
            if st.button("🔄 Retry Request", key="retry_connection"):
                st.experimental_rerun()
            return None

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ **Success!** Extracted {result.get('characters_extracted', 0):,} characters from {result.get('pages_processed', 0)} pages.")
            return result.get("extracted_text", "")
            
        elif response.status_code == 413:
            st.error("❌ **File too large** - Please use a smaller PDF file (max 100MB)")
            return None
            
        elif response.status_code == 400:
            try:
                error_detail = response.json().get("detail", "Bad request")
                st.error(f"❌ **Invalid file**: {error_detail}")
            except:
                st.error("❌ **Invalid file** - Please ensure you're uploading a valid PDF file")
            return None
            
        elif response.status_code == 500:
            st.error("❌ **Server error** - There was an issue processing your PDF. Please try again.")
            return None
            
        else:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except:
                error_detail = response.text[:200] + "..." if len(response.text) > 200 else response.text
            
            st.error(f"❌ **API Error ({response.status_code})**: {error_detail}")
            with st.expander("🔍 Technical Details"):
                st.code(f"""
Status Code: {response.status_code}
Request URL: {BACKEND_URL}/extract-pdf
File Name: {uploaded_file.name}
File Size: {file_size_mb:.1f}MB
Response: {response.text[:500]}
                """)
            
            return None
            
    except Exception as e:
        st.error(f"🚫 **Unexpected error**: {str(e)}")
        if st.button("🔄 Try Again", key="retry_unexpected"):
            st.experimental_rerun()
        
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
    st.markdown("""
        <div class="main-header">
            <h1>📄 Advanced Text Extractor</h1>
            <p>Extract text from <strong>PDF, DOCX, and TXT</strong> files with ease</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🔧 System Status")
        status_placeholder = st.empty()
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                status_placeholder.success("✅ Backend API is online")
                backend_online = True
            else:
                status_placeholder.error("❌ Backend API has issues")
                backend_online = False
        except:
            status_placeholder.error("❌ Backend API is offline")
            backend_online = False
        
        st.markdown("---")
        
        st.markdown("### ✨ Features")
        st.markdown("""
        - 🚀 **Fast Processing** - Quick text extraction
        - 📊 **Multiple Formats** - PDF, DOCX, TXT support  
        - 📈 **File Statistics** - Character, word, line counts
        - 💾 **Download Results** - Save extracted text
        - 🔒 **Secure** - Files processed safely
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - **PDF files**: Best results with text-based PDFs
        - **File size**: Keep under 100MB for faster processing
        - **Network**: Good connection recommended
        - **Retry**: If error occurs, wait 30s and retry
        """)

    if not backend_online:
        st.warning("⚠️ **Backend service is currently offline.** Please wait a moment and refresh the page.")
        if st.button("🔄 Refresh Status"):
            st.experimental_rerun()
    st.markdown("### 📁 Upload Your File")
    uploaded_file = st.file_uploader(
        "Choose a file to extract text from",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False,
        help="Select a PDF, DOCX, or TXT file. Maximum size: 100MB"
    )

    if uploaded_file:
        st.markdown("### 📋 File Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📄 File Name", 
                value=uploaded_file.name[:20] + "..." if len(uploaded_file.name) > 20 else uploaded_file.name
            )
        with col2:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.metric(
                label="📊 File Size", 
                value=f"{file_size_mb:.2f} MB" if file_size_mb >= 1 else f"{uploaded_file.size / 1024:.1f} KB"
            )
        with col3:
            file_type_display = {
                "application/pdf": "PDF Document",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word Document",
                "text/plain": "Text File"
            }
            st.metric(
                label="📝 Type", 
                value=file_type_display.get(uploaded_file.type, "Unknown")
            )
        with col4:
            if file_size_mb > 50:
                st.metric(label="⚡ Speed", value="Slow", delta="Large file")
            elif file_size_mb > 10:
                st.metric(label="⚡ Speed", value="Medium", delta=None)
            else:
                st.metric(label="⚡ Speed", value="Fast", delta="Small file")

        if file_size_mb > 100:
            st.error("❌ **File too large!** Please upload a file smaller than 100MB.")
            return
        elif file_size_mb > 50:
            st.warning("⚠️ **Large file detected.** Processing may take longer than usual.")

        text = None

        st.markdown("### 🔄 Processing")
        
        if uploaded_file.type == "application/pdf":
            if not backend_online:
                st.error("❌ Cannot process PDF: Backend service is offline")
                return
            text = extract_pdf_via_api(uploaded_file)
            
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_docx_text(uploaded_file)
            
        elif uploaded_file.type == "text/plain":
            text = extract_txt_text(uploaded_file)
        else:
            st.error("❌ **Unsupported file type!** Please upload a PDF, DOCX, or TXT file.")

        if text and text.strip():
            st.markdown("### 📖 Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            words = text.split()
            lines = text.split('\n')
            paragraphs = [p for p in text.split('\n\n') if p.strip()]
            
            with col1:
                st.metric("📝 Characters", f"{len(text):,}")
            with col2:
                st.metric("📊 Words", f"{len(words):,}")
            with col3:
                st.metric("📄 Lines", f"{len(lines):,}")
            with col4:
                st.metric("📋 Paragraphs", f"{len(paragraphs):,}")
            
            st.markdown("#### 👀 Text Preview")
            preview_length = st.slider("Preview length (characters)", 100, min(2000, len(text)), 500)
            preview_text = text[:preview_length] + ("..." if len(text) > preview_length else "")
            
            st.text_area(
                "Extracted Content", 
                preview_text, 
                height=300,
                help="This is a preview of your extracted text. Use the download button to get the full content."
            )

            
            st.markdown("### 📥 Download")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Ready to download your extracted text?**")
                st.markdown(f"Full text contains {len(text):,} characters")
            
            with col2:
                st.download_button(
                    label="📥 Download Full Text",
                    data=save_text_to_file(text, uploaded_file.name),
                    file_name=f"extracted_{os.path.splitext(uploaded_file.name)[0]}.txt",
                    mime="text/plain",
                    help="Download the complete extracted text as a .txt file"
                )
            
        elif text is not None:
            st.warning("⚠️ **No text content found** in the uploaded file. The file might be:")
            st.markdown("""
            - An image-based PDF (scanned document)
            - An empty or corrupted file
            - A file with only images or graphics
            """)

if __name__ == "__main__":
    main()  