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

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile):
    """Extract text from uploaded PDF file"""
    
    # Check file size
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 100MB)")

    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Read file contents
        contents = await file.read()
        
        # Extract text using pdfplumber
        with pdfplumber.open(BytesIO(contents)) as pdf:
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)