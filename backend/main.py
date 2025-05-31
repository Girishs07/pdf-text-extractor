from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from io import BytesIO
import uvicorn
import os

app = FastAPI(title="PDF Text Extractor API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # For development
        "https://pdf-text-extractor-2aombhdbxej9fyhxqmhr8m.streamlit.app/",  # Replace with your actual Streamlit app URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

@app.get("/")
async def root():
    return {"message": "PDF Text Extractor API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/test-upload")
async def test_upload(file: UploadFile):
    """Test endpoint to debug file uploads"""
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(await file.read()) if file else 0,
        "headers": dict(file.headers) if hasattr(file, 'headers') else {}
    }

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile):
    """Extract text from uploaded PDF file"""
    
    # Validate file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Check file size
    try:
        file.file.seek(0, 2)  # Move to end of file
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large ({file_size} bytes, max {MAX_FILE_SIZE} bytes)")

    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"Only PDF files are allowed. Received: {file.filename}")

    try:
        # Read file contents
        contents = await file.read()
        
        if not contents:
            raise HTTPException(status_code=400, detail="File content is empty")
        
        # Extract text using pdfplumber
        with pdfplumber.open(BytesIO(contents)) as pdf:
            if not pdf.pages:
                raise HTTPException(status_code=400, detail="PDF has no pages")
                
            extracted_pages = []
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_pages.append(f"--- Page {i+1} ---\n{page_text}")
            
            # Join all pages
            text = "\n\n".join(extracted_pages)
        
        if not text.strip():
            return {"extracted_text": "No text found in the PDF", "pages_processed": len(pdf.pages)}
        
        return {
            "extracted_text": text.strip(),
            "pages_processed": len(pdf.pages),
            "characters_extracted": len(text.strip())
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)