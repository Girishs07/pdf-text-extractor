import streamlit as st
from docx import Document
import os
import io 
from io import StringIO
import requests
import json

st.set_page_config(
    page_title="Advanced Text Extractor - Debug Mode",
    page_icon="🔧",
    layout="wide"
)

BACKEND_URL = "https://pdf-textextractor.onrender.com" 

# Debug function to test file before processing
def debug_file_upload(uploaded_file):
    """Debug the file upload to identify issues"""
    st.markdown("### 🔍 File Debug Information")
    
    debug_info = {}
    
    try:
        # Basic file info
        debug_info["filename"] = uploaded_file.name
        debug_info["file_type"] = uploaded_file.type
        debug_info["file_size"] = uploaded_file.size
        debug_info["file_size_mb"] = uploaded_file.size / (1024 * 1024)
        
        # Check file content
        uploaded_file.seek(0)
        first_bytes = uploaded_file.read(100)  # Read first 100 bytes
        uploaded_file.seek(0)  # Reset
        
        debug_info["first_bytes"] = first_bytes[:50].hex() if first_bytes else "No content"
        debug_info["is_pdf_header"] = first_bytes.startswith(b'%PDF') if first_bytes else False
        
        # Display debug info
        col1, col2 = st.columns(2)
        
        with col1:
            st.json({
                "filename": debug_info["filename"],
                "file_type": debug_info["file_type"],
                "file_size_bytes": debug_info["file_size"],
                "file_size_mb": round(debug_info["file_size_mb"], 3)
            })
        
        with col2:
            st.json({
                "has_pdf_header": debug_info["is_pdf_header"],
                "first_bytes_hex": debug_info["first_bytes"],
                "validations": {
                    "has_filename": bool(debug_info["filename"]),
                    "is_pdf_extension": debug_info["filename"].lower().endswith('.pdf'),
                    "size_under_100mb": debug_info["file_size_mb"] < 100,
                    "not_empty": debug_info["file_size"] > 0
                }
            })
        
        return debug_info
        
    except Exception as e:
        st.error(f"Debug error: {str(e)}")
        return None

def test_backend_debug_endpoint(uploaded_file):
    """Test the backend debug endpoint"""
    st.markdown("### 🔧 Backend Debug Test")
    
    try:
        uploaded_file.seek(0)
        files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
        
        with st.spinner("Testing backend debug endpoint..."):
            response = requests.post(
                f"{BACKEND_URL}/debug-upload",
                files=files,
                timeout=30
            )
        
        st.markdown("#### Backend Response:")
        if response.status_code == 200:
            st.success(f"✅ Debug endpoint successful (Status: {response.status_code})")
            st.json(response.json())
        else:
            st.error(f"❌ Debug endpoint failed (Status: {response.status_code})")
            try:
                st.json(response.json())
            except:
                st.text(response.text)
                
        return response
        
    except Exception as e:
        st.error(f"Debug endpoint error: {str(e)}")
        return None

def extract_pdf_via_api_debug(uploaded_file):
    """Extract text from PDF using the backend API with enhanced debugging"""
    try:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        st.markdown("### 📊 Pre-Upload Validation")
        
        # Pre-validation checks
        validations = {
            "File exists": uploaded_file is not None,
            "Has filename": bool(uploaded_file.name),
            "Is PDF extension": uploaded_file.name.lower().endswith('.pdf'),
            "Size under 100MB": file_size_mb < 100,
            "Not empty": uploaded_file.size > 0,
            "Correct MIME type": uploaded_file.type == "application/pdf"
        }
        
        for check, passed in validations.items():
            if passed:
                st.success(f"✅ {check}")
            else:
                st.error(f"❌ {check}")
        
        if not all(validations.values()):
            st.error("❌ Pre-validation failed. Cannot proceed with upload.")
            return None
        
        st.markdown("### 🚀 Uploading to Backend")
        
        uploaded_file.seek(0)
        
        # Prepare the exact same request as before
        files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔄 Sending request to backend...")
            progress_bar.progress(25)
            
            # Make the request with more detailed error handling
            response = requests.post(
                f"{BACKEND_URL}/extract-pdf", 
                files=files,
                timeout=300
            )
            
            progress_bar.progress(75)
            status_text.text("🔄 Processing response...")
            
            st.markdown("### 📋 Backend Response Details")
            st.write(f"**Status Code:** {response.status_code}")
            st.write(f"**Response Headers:** {dict(response.headers)}")
            
            progress_bar.progress(100)
            status_text.text("✅ Request completed!")
            
            # Clear progress indicators
            import time
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            # Handle response based on status code
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ **Success!** Extracted {result.get('characters_extracted', 0):,} characters from {result.get('pages_processed', 0)} pages.")
                return result.get("extracted_text", "")
                
            else:
                st.error(f"❌ **Request failed with status code {response.status_code}**")
                
                # Show detailed error information
                st.markdown("#### Error Details:")
                try:
                    error_data = response.json()
                    st.json(error_data)
                except:
                    st.text(response.text)
                
                # Show request details for debugging
                with st.expander("🔍 Request Debug Information"):
                    st.json({
                        "url": f"{BACKEND_URL}/extract-pdf",
                        "method": "POST",
                        "file_info": {
                            "name": uploaded_file.name,
                            "size": uploaded_file.size,
                            "type": uploaded_file.type
                        },
                        "response_status": response.status_code,
                        "response_headers": dict(response.headers)
                    })
                
                return None
            
        except requests.exceptions.Timeout:
            progress_bar.empty()
            status_text.empty()
            st.error("🚫 **Request timed out** - The PDF might be too large or complex.")
            return None
            
        except requests.exceptions.ConnectionError:
            progress_bar.empty()
            status_text.empty()
            st.error("🚫 **Connection failed** - Cannot reach the backend service.")
            return None
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"🚫 **Unexpected error**: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"🚫 **Function error**: {str(e)}")
        return None

def main():
    st.markdown("""
        # 🔧 PDF Text Extractor - Debug Mode
        This version includes enhanced debugging to identify the AxiosError 400 issue.
    """)
    
    # Backend status check
    with st.sidebar:
        st.markdown("### 🔧 Backend Status")
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend API is online")
                backend_online = True
            else:
                st.error(f"❌ Backend API returned {response.status_code}")
                backend_online = False
        except Exception as e:
            st.error(f"❌ Backend API is offline: {str(e)}")
            backend_online = False
    
    st.markdown("### 📁 Upload Your PDF File")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        accept_multiple_files=False,
        help="Select a PDF file for debugging"
    )

    if uploaded_file:
        # Debug the uploaded file
        debug_info = debug_file_upload(uploaded_file)
        
        if debug_info:
            st.markdown("---")
            
            # Test backend debug endpoint
            if st.button("🔧 Test Backend Debug Endpoint"):
                test_backend_debug_endpoint(uploaded_file)
            
            st.markdown("---")
            
            # Process with main endpoint
            if st.button("🚀 Process PDF (Main Endpoint)"):
                extract_pdf_via_api_debug(uploaded_file)

if __name__ == "__main__":
    main()