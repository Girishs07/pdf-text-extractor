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

# Backend API URL - Replace with your actual Render backend URL
BACKEND_URL = "https://pdf-textextractor.onrender.com"  # Update this!

# Custom CSS styling
st.markdown("""
    <style>
        /* Main app styling */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
        }
        
        /* Header styling */
        .main-header {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .main-header h1 {
            color: #2c3e50;
            font-size: 3em;
            margin-bottom: 0.5rem;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .main-header p {
            color: #7f8c8d;
            font-size: 1.2em;
        }
        
        /* File uploader styling */
        .stFileUploader {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        .stDownloadButton > button {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
            transition: all 0.3s ease;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        }
        
        /* Text area styling */
        .stTextArea textarea {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #333;
            padding: 15px;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            margin: 0.5rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Success/Error styling */
        .stSuccess {
            background: linear-gradient(90deg, #d4edda, #c3e6cb);
            border-left: 5px solid #28a745;
            border-radius: 5px;
            padding: 1rem;
        }
        
        .stError {
            background: linear-gradient(90deg, #f8d7da, #f5c6cb);
            border-left: 5px solid #dc3545;
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Loading animation */
        .loading-text {
            font-size: 1.2em;
            color: #667eea;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        /* File info cards */
        .file-info-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
    </style>
""", unsafe_allow_html=True)

def extract_pdf_via_api(uploaded_file):
    """Extract text from PDF using the backend API with robust error handling"""
    try:
        # Validate file size before sending
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > 100:
            st.error(f"❌ File too large: {file_size_mb:.1f}MB. Maximum allowed: 100MB")
            return None
        
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        # Prepare file for API request
        files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
        
        # Show progress and status
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Connecting
            status_text.text("🔄 Connecting to backend...")
            progress_bar.progress(25)
            
            # Make API request with retries
            response = requests.post(
                f"{BACKEND_URL}/extract-pdf", 
                files=files,
                timeout=300  # 5 minutes timeout
            )
            
            # Step 2: Processing
            status_text.text("🔄 Processing PDF...")
            progress_bar.progress(75)
            
            # Step 3: Complete
            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")
            
            # Clear progress indicators
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
            # Enhanced error handling with retry option
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except:
                error_detail = response.text[:200] + "..." if len(response.text) > 200 else response.text
            
            st.error(f"❌ **API Error ({response.status_code})**: {error_detail}")
            
            # Debug information in expander
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
        
        # Show retry button for unexpected errors
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
    # Custom header
    st.markdown("""
        <div class="main-header">
            <h1>📄 Advanced Text Extractor</h1>
            <p>Extract text from <strong>PDF, DOCX, and TXT</strong> files with ease</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 🔧 System Status")
        
        # Backend status check with better UI
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
        
        # Feature highlights
        st.markdown("### ✨ Features")
        st.markdown("""
        - 🚀 **Fast Processing** - Quick text extraction
        - 📊 **Multiple Formats** - PDF, DOCX, TXT support  
        - 📈 **File Statistics** - Character, word, line counts
        - 💾 **Download Results** - Save extracted text
        - 🔒 **Secure** - Files processed safely
        """)
        
        st.markdown("---")
        
        # Usage tips
        st.markdown("### 💡 Tips")
        st.markdown("""
        - **PDF files**: Best results with text-based PDFs
        - **File size**: Keep under 100MB for faster processing
        - **Network**: Good connection recommended
        - **Retry**: If error occurs, wait 30s and retry
        """)

    # Main content area
    if not backend_online:
        st.warning("⚠️ **Backend service is currently offline.** Please wait a moment and refresh the page.")
        if st.button("🔄 Refresh Status"):
            st.experimental_rerun()
    
    # File uploader with improved styling
    st.markdown("### 📁 Upload Your File")
    uploaded_file = st.file_uploader(
        "Choose a file to extract text from",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False,
        help="Select a PDF, DOCX, or TXT file. Maximum size: 100MB"
    )

    if uploaded_file:
        # Enhanced file information display
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
            # Processing status indicator
            if file_size_mb > 50:
                st.metric(label="⚡ Speed", value="Slow", delta="Large file")
            elif file_size_mb > 10:
                st.metric(label="⚡ Speed", value="Medium", delta=None)
            else:
                st.metric(label="⚡ Speed", value="Fast", delta="Small file")

        # File size warning
        if file_size_mb > 100:
            st.error("❌ **File too large!** Please upload a file smaller than 100MB.")
            return
        elif file_size_mb > 50:
            st.warning("⚠️ **Large file detected.** Processing may take longer than usual.")

        text = None

        # Process different file types with improved feedback
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

        # Enhanced results display
        if text and text.strip():
            st.markdown("### 📖 Results")
            
            # Text statistics with better layout
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
            
            # Text preview with improved styling
            st.markdown("#### 👀 Text Preview")
            preview_length = st.slider("Preview length (characters)", 100, min(2000, len(text)), 500)
            preview_text = text[:preview_length] + ("..." if len(text) > preview_length else "")
            
            st.text_area(
                "Extracted Content", 
                preview_text, 
                height=300,
                help="This is a preview of your extracted text. Use the download button to get the full content."
            )

            # Download section with better styling
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